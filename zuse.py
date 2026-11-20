#!/usr/bin/env python3
import os
import sys
import json
import requests
import re
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from tools.executor import execute_command

console = Console()
API_KEY = os.getenv("AI_API_KEY")
MODEL = "qwen/qwen3.8-27b" 
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Đọc tất cả Skill trong thư mục
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
Bạn là một hệ thống Multi-Agent, có khả năng tự động viết code, test và sửa lỗi.

Dưới đây là các KỸ NĂNG (Skills) bạn có thể sử dụng:
{SKILLS_PROMPT}

Bạn PHẢI phản hồi theo định dạng JSON chính xác như sau:
- Viết file: {{"action": "write", "path": "tên_file.py", "content": "code"}}
- Chạy lệnh: {{"action": "run", "command": "python tên_file.py"}}
- Hoàn thành: {{"action": "done", "content": "Báo cáo kết quả"}}

Hãy suy nghĩ từng bước một. Khi viết code, hãy chú ý áp dụng các Skill đã được dạy.
"""

def show_banner():
    banner = Panel.fit(
        "[bold cyan]🧠 ZUSE CODER AI v2.0[/bold cyan]\n"
        "[green]Hệ thống AI Đa Tác Vụ (Multi-Agent)[/green]\n"
        "[yellow]Gõ /help để xem các lệnh[/yellow]",
        title="[bold magenta]HỆ ĐIỀU HÀNH AI[/bold magenta]",
        border_style="cyan"
    )
    console.print(banner)

def call_ai(messages):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": MODEL, "messages": messages}
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        return r.json()['choices'][0]['message']['content']
    except Exception as e:
        console.print(f"[bold red]❌ Lỗi API: {e}[/bold red]")
        return None

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try: return json.loads(match.group(0))
        except: return None
    return None

def main():
    if not API_KEY:
        console.print("[bold red]❌ Thiếu AI_API_KEY. Chạy: export AI_API_KEY='...'[/bold red]")
        sys.exit(1)

    show_banner()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            user_input = console.input("\n[bold green]Zuse > [/bold green]").strip()
            
            if not user_input: continue
            if user_input == "/exit": break
            
            # Xử lý Slash Commands
            if user_input.startswith("/"):
                cmd = user_input.split()[0]
                if cmd == "/help":
                    console.print("[cyan]/help: Xem trợ giúp | /clear: Xóa lịch sử | /exec <lệnh>: Chạy lệnh trực tiếp | /skills: Xem danh sách skill[/cyan]")
                elif cmd == "/clear":
                    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                    console.print("[yellow]Đã xóa lịch sử hội thoại.[/yellow]")
                elif cmd == "/skills":
                    console.print(f"[cyan]Đã nạp {len(SKILLS_PROMPT)} ký tự kỹ năng từ thư mục skills/[/cyan]")
                elif cmd == "/exec":
                    command = user_input.replace("/exec", "").strip()
                    out, err, code = execute_command(command)
                    console.print(Panel(out + err, title=f"Exit code: {code}", border_style="yellow"))
                else:
                    console.print("[red]Lệnh không hợp lệ. Gõ /help[/red]")
                continue

            # Thêm lệnh của user vào lịch sử
            messages.append({"role": "user", "content": user_input})
            
            # Vòng lặp Agent
            for step in range(10):
                with console.status(f"[bold cyan]Zuse đang suy nghĩ (Bước {step+1})...[/bold cyan]"):
                    response = call_ai(messages)
                
                if not response: break
                
                json_res = extract_json(response)
                if not json_res:
                    console.print("[red]AI trả lời sai JSON. Đang thử lại...[/red]")
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
