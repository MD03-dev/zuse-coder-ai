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
from rich.prompt import Prompt
from tools.executor import execute_command

console = Console()
API_KEY = os.getenv("AI_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Danh sách model
AVAILABLE_MODELS = {
    "1": "llama-3.1-8b-instant",
    "2": "llama-3.3-70b-versatile",
    "3": "qwen/qwen3.8-27b",
    "4": "openai/gpt-oss-120b",
    "5": "openai/gpt-oss-20b",
    "6": "meta-llama/llama-4-scout-17b-16e-instruct",
    "7": "mixtral-8x7b-32768"
}

CURRENT_MODEL = "llama-3.1-8b-instant"
LANGUAGES = {"1": "Vietnamese", "2": "English", "3": "Chinese", "4": "Russian", "5": "Japanese"}
CURRENT_LANG = "Vietnamese"

def load_skills():
    skills_text = ""
    if os.path.exists("skills"):
        for f in os.listdir("skills"):
            if f.endswith(".md"):
                with open(f"skills/{f}", "r", encoding="utf-8") as file:
                    skills_text += f"\n[SKILL: {f}]\n{file.read()}\n"
    return skills_text

SKILLS_PROMPT = load_skills()

def get_system_prompt():
    return f"""Bạn là Zuse, AI Coder chạy trên Termux. Ngôn ngữ giao tiếp hiện tại: {CURRENT_LANG}.
Hãy viết code ngắn gọn, súc tích.
Khi người dùng yêu cầu code, PHẢI dùng action "write" rồi đến "run".
Định dạng JSON:
- {{"action": "write", "path": "tên_file.py", "content": "code"}}
- {{"action": "run", "command": "python tên_file.py"}}
- {{"action": "done", "content": "Báo cáo"}}
Kỹ năng: {SKILLS_PROMPT}
"""

def show_banner():
    os.system('clear')
    banner_text = f"""
[bold cyan]
███████╗██╗   ██╗███████╗███████╗
╚══███╔╝██║   ██║██╔════╝██╔════╝
  ███╔╝ ██║   ██║███████╗█████╗  
 ███╔╝  ██║   ██║╚════██║██╔══╝  
███████╗╚██████╔╝███████║███████╗
╚══════╝ ╚═════╝ ╚══════╝╚══════╝
[/bold cyan]
[bold green]HỆ ĐIỀU HÀNH AI ĐA TÁC VỤ (MULTI-AGENT)[/bold green]
[bold yellow]🤖 Model: {CURRENT_MODEL} | 🌐 Ngôn ngữ: {CURRENT_LANG}[/bold yellow]
"""
    console.print(Panel(banner_text, title="[bold magenta]ZUSE CODER AI v5.0[/bold magenta]", border_style="cyan", expand=False))
    
    # Hướng dẫn chi tiết cho /help
    t1 = Table(title="Lệnh Hệ Thống", title_style="bold yellow", show_header=True)
    t1.add_column("Lệnh", style="cyan", width=15)
    t1.add_column("Chức năng", style="green")
    t1.add_row("/help", "Xem trợ giúp chi tiết")
    t1.add_row("/exit", "Thoát chương trình")
    t1.add_row("/model", "Đổi Model AI (nếu hết token)")
    t1.add_row("/lang", "Đổi ngôn ngữ giao tiếp")
    t1.add_row("/clear", "Xóa lịch sử chat")

    t2 = Table(title="Lệnh Tiện Ích", title_style="bold yellow", show_header=True)
    t2.add_column("Lệnh", style="cyan", width=15)
    t2.add_column("Chức năng", style="green")
    t2.add_row("/exec <lệnh>", "Chạy lệnh Terminal")
    t2.add_row("/ls", "Xem danh sách file")
    t2.add_row("/cat <file>", "Đọc nội dung file")
    t2.add_row("/sysinfo", "Xem thông tin thiết bị")
    t2.add_row("/tokens", "Hướng dẫn xử lý hết token")

    console.print(t1)
    console.print(t2)
    console.print("[dim]Gõ /help để xem hướng dẫn xử lý khi hết token (Rate Limit)[/dim]\n")

def call_ai(messages):
    global CURRENT_MODEL
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": CURRENT_MODEL, "messages": messages}
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        data = r.json()
        
        if 'error' in data:
            err_msg = data['error'].get('message', '')
            if 'Rate limit' in err_msg or 'Request too large' in err_msg:
                console.print(f"[bold red]❌ Lỗi: Đã hết Token/Phút (Rate Limit) của model {CURRENT_MODEL}![/bold red]")
                console.print("[yellow]👉 Gợi ý: Gõ lệnh /model để đổi sang model khác (VD: Llama 3.1 8B) hoặc đợi 1 phút rồi thử lại.[/yellow]")
            elif 'Invalid API Key' in err_msg:
                console.print(f"[bold red]❌ Lỗi API Key: Hãy dùng key Groq (gsk_...)![/bold red]")
            elif 'does not exist' in err_msg:
                console.print(f"[bold red]❌ Model {CURRENT_MODEL} không tồn tại hoặc chưa được cấp quyền.[/bold red]")
                console.print("[yellow]👉 Hãy gõ /model để chọn model khác.[/yellow]")
            else:
                console.print(f"[bold red]❌ Lỗi API: {err_msg}[/bold red]")
            return None
            
        return data['choices'][0]['message']['content']
    except Exception as e:
        console.print(f"[bold red]❌ Lỗi kết nối mạng: {e}[/bold red]")
        return None

def extract_json(text):
    # Tìm JSON, xử lý cả trường hợp AI trả về có dấu ```json ... ```
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try: return json.loads(match.group(0))
        except: return None
    return None

def change_model():
    global CURRENT_MODEL
    console.print("\n[bold cyan]DANH SÁCH MODEL GROQ:[/bold cyan]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("STT", width=5)
    table.add_column("Tên Model", style="green")
    table.add_column("Ghi chú", style="yellow")
    
    notes = {
        "1": "Siêu nhanh, ít tốn token (Mặc định)",
        "2": "Thông minh nhất, viết code đỉnh (Rất tốn token)",
        "3": "Cân bằng, tốt cho tiếng Việt",
        "4": "Model mới, suy luận cực mạnh",
        "5": "Model nhẹ của OpenAI",
        "6": "Llama 4 thế hệ mới",
        "7": "Mixtral"
    }
    
    for k, v in AVAILABLE_MODELS.items():
        table.add_row(k, v, notes.get(k, ""))
    console.print(table)
    
    choice = Prompt.ask("[bold green]Chọn số thứ tự để đổi model (hoặc 0 để hủy)[/bold green]")
    if choice in AVAILABLE_MODELS:
        CURRENT_MODEL = AVAILABLE_MODELS[choice]
        console.print(f"[bold green]✅ Đã đổi sang model: {CURRENT_MODEL}[/bold green]")
    elif choice == "0":
        console.print("[yellow]Đã hủy.[/yellow]")
    else:
        console.print("[red]Lựa chọn không hợp lệ.[/red]")

def change_language():
    global CURRENT_LANG
    console.print("\n[bold cyan]CHỌN NGÔN NGỮ GIAO TIẾP:[/bold cyan]")
    for k, v in LANGUAGES.items():
        console.print(f"[{k}] {v}")
    
    choice = Prompt.ask("[bold green]Chọn ngôn ngữ (1-5)[/bold green]")
    if choice in LANGUAGES:
        CURRENT_LANG = LANGUAGES[choice]
        console.print(f"[bold green]✅ Đã đổi sang ngôn ngữ: {CURRENT_LANG}[/bold green]")
    else:
        console.print("[red]Lựa chọn không hợp lệ.[/red]")

def help_tokens():
    console.print(Panel(
        "[bold yellow]HƯỚNG DẪN XỬ LÝ KHI HẾT TOKEN (RATE LIMIT)[/bold yellow]\n\n"
        "1. Groq giới hạn số lượng Token mỗi phút (TPM) tùy theo Model.\n"
        "2. Model càng thông minh (như 70B, 120B) càng tốn nhiều Token.\n"
        "3. Nếu gặp lỗi [red]Rate limit[/red] hoặc [red]Request too large[/red]:\n"
        "   - Cách 1: Đợi 1 phút rồi thử lại.\n"
        "   - Cách 2: Gõ lệnh [cyan]/model[/cyan] và chọn số [green]1[/green] (Llama 3.1 8B) để dùng model nhẹ, ít tốn token hơn.\n"
        "   - Cách 3: Chia nhỏ yêu cầu của bạn ra (ví dụ: yêu cầu viết từng hàm một thay vì cả file dài).",
        title="[bold red]Xử lý lỗi Token[/bold red]",
        border_style="red"
    ))

def main():
    if not API_KEY:
        console.print("[bold red]❌ Thiếu AI_API_KEY. Chạy: export AI_API_KEY='gsk_...'[/bold red]")
        sys.exit(1)

    show_banner()
    messages = [{"role": "system", "content": get_system_prompt()}]

    while True:
        try:
            user_input = console.input("\n[bold green]Zuse > [/bold green]").strip()
            if not user_input: continue
            if user_input == "/exit": break
            
            if user_input.startswith("/"):
                cmd = user_input.split()[0]
                
                if cmd == "/help":
                    show_banner()
                elif cmd == "/tokens":
                    help_tokens()
                elif cmd == "/model":
                    change_model()
                    messages = [{"role": "system", "content": get_system_prompt()}] # Cập nhật lại prompt
                elif cmd == "/lang":
                    change_language()
                    messages = [{"role": "system", "content": get_system_prompt()}] # Cập nhật lại prompt
                elif cmd == "/clear":
                    messages = [{"role": "system", "content": get_system_prompt()}]
                    console.print("[yellow]Đã xóa lịch sử chat.[/yellow]")
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
                else:
                    console.print("[red]Lệnh không hợp lệ. Gõ /help để xem.[/red]")
                continue

            messages.append({"role": "user", "content": user_input})
            
            for step in range(10):
                with console.status(f"[bold cyan]Zuse ({CURRENT_MODEL}) đang suy nghĩ...[/bold cyan]"):
                    response = call_ai(messages)
                
                if not response: break
                
                json_res = extract_json(response)
                if not json_res:
                    # Nếu AI trả lời chat thay vì JSON, ta in ra và nhắc nó
                    console.print(f"[bold yellow]🤖 Zuse:[/bold yellow] {response}")
                    messages.append({"role": "assistant", "content": response})
                    messages.append({"role": "user", "content": "Lỗi: Bạn phải trả về đúng định dạng JSON để tôi có thể thực thi code."})
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
