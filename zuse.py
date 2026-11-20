#!/usr/bin/env python3
import os
import sys
import json
import requests
import re
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from tools.executor import execute_command

console = Console()
API_KEY = os.getenv("AI_API_KEY")
# Đổi sang model 8b cho nhẹ và ít bị giới hạn token
MODEL = "llama-3.1-8b-instant" 
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
SYSTEM_PROMPT = f"""Bạn là Zuse, AI Coder chạy trên Termux. Hãy viết code ngắn gọn, súc tích để tránh bị giới hạn token.
Khi người dùng yêu cầu code, PHẢI dùng action "write" rồi đến "run".
Định dạng JSON:
- {{"action": "write", "path": "tên_file.py", "content": "code"}}
- {{"action": "run", "command": "python tên_file.py"}}
- {{"action": "done", "content": "Báo cáo"}}
Kỹ năng: {SKILLS_PROMPT}
"""

def show_banner():
    # Xóa màn hình cũ
    os.system('clear')
    
    banner_text = """
[bold cyan]
███████╗██╗   ██╗███████╗███████╗
╚══███╔╝██║   ██║██╔════╝██╔════╝
  ███╔╝ ██║   ██║███████╗█████╗  
 ███╔╝  ██║   ██║╚════██║██╔══╝  
███████╗╚██████╔╝███████║███████╗
╚══════╝ ╚═════╝ ╚══════╝╚══════╝
[/bold cyan]
[bold green]HỆ ĐIỀU HÀNH AI ĐA TÁC VỤ (MULTI-AGENT)[/bold green]
[dim]Model hiện tại: llama-3.1-8b-instant | Không cần root[/dim]
"""
    console.print(Panel(banner_text, title="[bold magenta]ZUSE CODER AI v3.0[/bold magenta]", border_style="cyan", expand=False))
    
    # Bảng 1: Cơ bản
    t1 = Table(title="Lệnh Cơ Bản", title_style="bold yellow", show_header=True, header_style="bold magenta")
    t1.add_column("Lệnh", style="cyan", width=15)
    t1.add_column("Chức năng", style="green")
    t1.add_row("/help", "Xem trợ giúp")
    t1.add_row("/exit", "Thoát chương trình")
    t1.add_row("/clear", "Xóa lịch sử chat")
    t1.add_row("/reset", "Khởi động lại AI")

    # Bảng 2: Hệ thống
    t2 = Table(title="Hệ Thống & File", title_style="bold yellow", show_header=True, header_style="bold magenta")
    t2.add_column("Lệnh", style="cyan", width=15)
    t2.add_column("Chức năng", style="green")
    t2.add_row("/exec <lệnh>", "Chạy lệnh Terminal")
    t2.add_row("/ls", "Xem danh sách file")
    t2.add_row("/cat <file>", "Đọc nội dung file")
    t2.add_row("/rm <file>", "Xóa file")

    # Bảng 3: AI & Skills
    t3 = Table(title="AI & Kỹ Năng", title_style="bold yellow", show_header=True, header_style="bold magenta")
    t3.add_column("Lệnh", style="cyan", width=15)
    t3.add_column("Chức năng", style="green")
    t3.add_row("/skills", "Xem kỹ năng đã nạp")
    t3.add_row("/model", "Xem model đang dùng")
    t3.add_row("/system", "Xem Prompt hệ thống")
    t3.add_row("/history", "Xem lịch sử chat")

    # Bảng 4: Tiện ích
    t4 = Table(title="Tiện Ích", title_style="bold yellow", show_header=True, header_style="bold magenta")
    t4.add_column("Lệnh", style="cyan", width=15)
    t4.add_column("Chức năng", style="green")
    t4.add_row("/ping", "Kiểm tra mạng")
    t4.add_row("/time", "Xem giờ hệ thống")
    t4.add_row("/sysinfo", "Xem thông tin thiết bị")
    t4.add_row("/df", "Xem dung lượng ổ đĩa")

    console.print(t1)
    console.print(t2)
    console.print(t3)
    console.print(t4)
    console.print("[dim]Gõ câu lệnh thường để AI viết code. Ví dụ: viet ham tinh tong[/dim]\n")

def call_ai(messages):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": MODEL, "messages": messages}
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        data = r.json()
        
        if 'error' in data:
            err_msg = data['error'].get('message', '')
            if 'Rate limit' in err_msg or 'Request too large' in err_msg:
                console.print(f"[bold red]❌ Lỗi: Bạn đã dùng quá giới hạn token/phút của Groq. Vui lòng đợi 1 phút rồi thử lại![/bold red]")
            elif 'Invalid API Key' in err_msg or 'Unauthorized' in err_msg:
                console.print(f"[bold red]❌ Lỗi API Key: Hãy dùng key Groq (gsk_...)![/bold red]")
            else:
                console.print(f"[bold red]❌ Lỗi API: {err_msg}[/bold red]")
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
            
            # Xử lý Slash Commands
            if user_input.startswith("/"):
                cmd = user_input.split()[0]
                
                if cmd == "/help":
                    show_banner()
                elif cmd == "/clear" or cmd == "/reset":
                    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                    console.print("[yellow]Đã xóa lịch sử chat.[/yellow]")
                elif cmd == "/skills":
                    console.print(f"[cyan]Đã nạp kỹ năng từ thư mục skills/[/cyan]")
                elif cmd == "/model":
                    console.print(f"[cyan]Model hiện tại: {MODEL}[/cyan]")
                elif cmd == "/system":
                    console.print(Panel(SYSTEM_PROMPT, title="System Prompt", border_style="dim"))
                elif cmd == "/ls":
                    out, err, _ = execute_command("ls -la")
                    console.print(Panel(out + err, title="Danh sách file", border_style="dim"))
                elif cmd == "/cat":
                    file_name = user_input.replace("/cat", "").strip()
                    out, err, _ = execute_command(f"cat {file_name}")
                    console.print(Panel(out + err, title=f"Nội dung {file_name}", border_style="dim"))
                elif cmd == "/exec":
                    command = user_input.replace("/exec", "").strip()
                    out, err, code = execute_command(command)
                    console.print(Panel(out + err, title=f"Exit code: {code}", border_style="yellow"))
                elif cmd == "/sysinfo":
                    out, err, _ = execute_command("uname -a && free -h")
                    console.print(Panel(out + err, title="Thông tin thiết bị", border_style="dim"))
                elif cmd == "/df":
                    out, err, _ = execute_command("df -h")
                    console.print(Panel(out + err, title="Dung lượng", border_style="dim"))
                elif cmd == "/time":
                    out, err, _ = execute_command("date")
                    console.print(Panel(out + err, title="Thời gian", border_style="dim"))
                elif cmd == "/ping":
                    out, err, _ = execute_command("ping -c 3 google.com")
                    console.print(Panel(out + err, title="Ping", border_style="dim"))
                elif cmd == "/history":
                    history_str = "\n".join([f"{m['role']}: {m['content'][:50]}..." for m in messages[1:]])
                    console.print(Panel(history_str if history_str else "Trống", title="Lịch sử", border_style="dim"))
                else:
                    console.print("[red]Lệnh không hợp lệ. Gõ /help để xem danh sách.[/red]")
                continue

            # Xử lý chat bình thường
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
