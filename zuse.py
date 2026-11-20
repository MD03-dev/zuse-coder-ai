#!/usr/bin/env python3
import os
import sys
import json
import requests
import re
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from tools.executor import execute_command

console = Console()
API_KEY = os.getenv("AI_API_KEY")
MODEL = "qwen/qwen3.8-27b" 
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def load_skills():
    skills_text = ""
    if os.path.exists("skills"):
        for f in os.listdir("skills"):
            if f.endswith(".md"):
                with open(f"skills/{f}", "r", encoding="utf-8") as file:
                    skills_text += f"\n[SKILL: {f}]\n{file.read()}\n"
    return skills_text

SKILLS_PROMPT = load_skills()
SYSTEM_PROMPT = f"""Bạn là Zuse, một AI Coder chuyên nghiệp cấp cao chạy trên hệ điều hành Termux.
Bạn PHẢI phản hồi theo định dạng JSON chính xác như sau:
- Viết file: {{"action": "write", "path": "tên_file.py", "content": "code"}}
- Chạy lệnh: {{"action": "run", "command": "python tên_file.py"}}
- Hoàn thành: {{"action": "done", "content": "Báo cáo kết quả"}}
Kỹ năng của bạn: {SKILLS_PROMPT}
"""

def show_banner():
    banner = Panel.fit(
        "[bold cyan]🧠 ZUSE CODER AI v2.0[/bold cyan]\n"
        "[green]Hệ thống AI Đa Tác Vụ (Multi-Agent)[/green]\n"
        "[yellow]Model: qwen/qwen3.8-27b[/yellow]",
        title="[bold magenta]HỆ ĐIỀU HÀNH AI[/bold magenta]",
        border_style="cyan"
    )
    console.print(banner)
    
    # Bảng hiển thị danh sách lệnh
    table = Table(title="Danh sách lệnh (Slash Commands)", title_style="bold yellow")
    table.add_column("Lệnh", style="cyan", no_wrap=True)
    table.add_column("Chức năng", style="green")
    table.add_row("/help", "Xem trợ giúp")
    table.add_row("/clear", "Xóa lịch sử hội thoại")
    table.add_row("/exec <lệnh>", "Chạy lệnh trực tiếp trên Terminal")
    table.add_row("/skills", "Xem các kỹ năng AI đang có")
    table.add_row("/exit", "Thoát chương trình")
    console.print(table)
    console.print("[dim]Gõ câu lệnh bình thường (không cần dấu /) để AI viết code.[/dim]\n")

def call_ai(messages):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": MODEL, "messages": messages}
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        data = r.json()
        
        # Kiểm tra lỗi API Key
        if 'error' in data:
            err_msg = data['error'].get('message', '')
            if 'Invalid API Key' in err_msg or 'Unauthorized' in err_msg:
                console.print(f"[bold red]❌ LỖI API KEY: Bạn đang dùng sai key! Hãy dùng key Groq (bắt đầu bằng gsk_...), không phải token GitHub (ghp_...).[/bold red]")
            else:
                console.print(f"[bold red]❌ Lỗi API: {err_msg}[/bold red]")
            return None
            
        if 'choices' not in data:
            console.print(f"[bold red]❌ Lỗi API (Không có choices): {data}[/bold red]")
            return None
            
        return data['choices'][0]['message']['content']
    except Exception as e:
        console.print(f"[bold red]❌ Lỗi kết nối mạng: {e}[/bold red]")
        return None

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try: return json.loads(match.group(0))
        except: return None
    return None

def main():
    if not API_KEY:
        console.print("[bold red]❌ Thiếu AI_API_KEY. Chạy: export AI_API_KEY='gsk_...'[/bold red]")
        sys.exit(1)

    show_banner()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            user_input = console.input("\n[bold green]Zuse > [/bold green]").strip()
            if not user_input: continue
            if user_input == "/exit": break
            
            if user_input.startswith("/"):
                cmd = user_input.split()[0]
                if cmd == "/help":
                    console.print("[cyan]Gõ /clear, /exec, /skills, /exit để điều khiển.[/cyan]")
                elif cmd == "/clear":
                    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                    console.print("[yellow]Đã xóa lịch sử.[/yellow]")
                elif cmd == "/skills":
                    console.print(f"[cyan]Đã nạp kỹ năng từ thư mục skills/[/cyan]")
                elif cmd == "/exec":
                    command = user_input.replace("/exec", "").strip()
                    out, err, code = execute_command(command)
                    console.print(Panel(out + err, title=f"Exit code: {code}", border_style="yellow"))
                else:
                    console.print("[red]Lệnh không hợp lệ.[/red]")
                continue

            messages.append({"role": "user", "content": user_input})
            
            for step in range(10):
                with console.status(f"[bold cyan]Zuse đang suy nghĩ (Bước {step+1})...[/bold cyan]"):
                    response = call_ai(messages)
                
                if not response: break
                
                json_res = extract_json(response)
                if not json_res:
                    messages.append({"role": "assistant", "content": response})
                    messages.append({"role": "user", "content": "Lỗi định dạng. Hãy trả về JSON."})
                    continue

                messages.append({"role": "assistant", "content": response})
                action = json_res.get("action")

                if action == "write":
                    path = json_res.get("path")
                    content = json_res.get("content")
                    console.print(f"[green]✍️ Ghi file:[/green] {path}")
                    with open(path, "w", encoding="utf-8") as f: f.write(content)
                    messages.append({"role": "user", "content": f"Đã ghi file {path}. Hãy chạy thử."})
                
                elif action == "run":
                    cmd = json_res.get("command")
                    console.print(f"[yellow]⚙️ Đang chạy:[/yellow] {cmd}")
                    out, err, code = execute_command(cmd)
                    output = out + err
                    if output.strip():
                        console.print(Panel(output.strip(), title="Terminal Output", border_style="dim"))
                    
                    if code == 0:
                        console.print("[green]✅ Chạy thành công![/green]")
                        messages.append({"role": "user", "content": f"Chạy thành công. Output: {output}"})
                    else:
                        console.print("[red]❌ Có lỗi xảy ra, AI sẽ tự sửa![/red]")
                        messages.append({"role": "user", "content": f"Lỗi: {output}. Hãy sửa code và chạy lại."})

                elif action == "done":
                    console.print(f"\n[bold green]🤖 Zuse:[/bold green] {json_res.get('content')}")
                    break

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
