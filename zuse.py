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

# --- TỐI ƯU TOKEN: Rút gọn System Prompt tối đa ---
def get_system_prompt():
    return f"""Bạn là Zuse, AI Coder Termux. Ngôn ngữ: {CURRENT_LANG}.
Quy tắc bắt buộc: Chỉ trả về JSON.
- Viết file: {{"action": "write", "path": "f.py", "content": "code"}}
- Chạy: {{"action": "run", "command": "python f.py"}}
- Xong: {{"action": "done", "content": "msg"}}
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
[bold green]ZUSE CODER AI v6.0 - Token Optimized[/bold green]
[bold yellow]🤖 Model: {CURRENT_MODEL} | 🌐 Ngôn ngữ: {CURRENT_LANG}[/bold yellow]
"""
    console.print(Panel(banner_text, title="[bold magenta]HỆ ĐIỀU HÀNH AI[/bold magenta]", border_style="cyan", expand=False))
    
    t1 = Table(title="Lệnh Hệ Thống", title_style="bold yellow")
    t1.add_column("Lệnh", style="cyan", width=15)
    t1.add_column("Chức năng", style="green")
    t1.add_row("/help", "Xem trợ giúp")
    t1.add_row("/model", "Đổi Model AI")
    t1.add_row("/lang", "Đổi ngôn ngữ")
    t1.add_row("/clear", "Xóa lịch sử (tiết kiệm token)")
    t1.add_row("/exit", "Thoát")

    t2 = Table(title="Tiện Ích", title_style="bold yellow")
    t2.add_column("Lệnh", style="cyan", width=15)
    t2.add_column("Chức năng", style="green")
    t2.add_row("/exec <lệnh>", "Chạy lệnh")
    t2.add_row("/ls", "Xem file")
    t2.add_row("/cat <file>", "Đọc file")
    t2.add_row("/tokens", "Hướng dẫn tiết kiệm token")

    console.print(t1)
    console.print(t2)
    console.print("[dim]Gõ /tokens để xem mẹo tiết kiệm token.[/dim]\n")

# --- TỐI ƯU TOKEN: Cắt bớt lịch sử chat cũ ---
def trim_history(messages):
    # Giữ lại system prompt và tối đa 6 tin nhắn gần nhất
    if len(messages) > 7:
        return [messages[0]] + messages[-6:]
    return messages

def call_ai(messages):
    global CURRENT_MODEL
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    # Cắt tỉa lịch sử trước khi gửi
    trimmed_messages = trim_history(messages)
    payload = {"model": CURRENT_MODEL, "messages": trimmed_messages}
    
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        data = r.json()
        
        if 'error' in data:
            err_msg = data['error'].get('message', '')
            if 'Rate limit' in err_msg or 'Request too large' in err_msg:
                console.print(f"[bold red]❌ Hết Token/Phút! Hãy gõ /model chọn số 1 hoặc /clear để xóa lịch sử.[/bold red]")
            elif 'Invalid API Key' in err_msg:
                console.print(f"[bold red]❌ Lỗi API Key![/bold red]")
            elif 'does not exist' in err_msg:
                console.print(f"[bold red]❌ Model {CURRENT_MODEL} không tồn tại.[/bold red]")
            else:
                console.print(f"[bold red]❌ Lỗi API: {err_msg}[/bold red]")
            return None
            
        return data['choices'][0]['message']['content']
    except Exception as e:
        console.print(f"[bold red]❌ Lỗi mạng: {e}[/bold red]")
        return None

def extract_json(text):
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
        "1": "Siêu nhanh, tiết kiệm token nhất",
        "2": "Thông minh nhất (Tốn token cực nhiều)",
        "3": "Cân bằng",
        "4": "Model lớn của OpenAI",
        "5": "Model nhỏ của OpenAI",
        "6": "Llama 4",
        "7": "Mixtral"
    }
    
    for k, v in AVAILABLE_MODELS.items():
        table.add_row(k, v, notes.get(k, ""))
    console.print(table)
    
    choice = Prompt.ask("[bold green]Chọn số thứ tự (0 để hủy)[/bold green]")
    if choice in AVAILABLE_MODELS:
        CURRENT_MODEL = AVAILABLE_MODELS[choice]
        console.print(f"[bold green]✅ Đã đổi sang: {CURRENT_MODEL}[/bold green]")
    elif choice != "0":
        console.print("[red]Không hợp lệ.[/red]")

def change_language():
    global CURRENT_LANG
    console.print("\n[bold cyan]CHỌN NGÔN NGỮ:[/bold cyan]")
    for k, v in LANGUAGES.items():
        console.print(f"[{k}] {v}")
    choice = Prompt.ask("[bold green]Chọn (1-5)[/bold green]")
    if choice in LANGUAGES:
        CURRENT_LANG = LANGUAGES[choice]
        console.print(f"[bold green]✅ Đã đổi sang: {CURRENT_LANG}[/bold green]")

def help_tokens():
    console.print(Panel(
        "[bold yellow]MẸO TIẾT KIỆM TOKEN TỐI ĐA[/bold yellow]\n\n"
        "1. [cyan]/clear[/cyan]: Xóa lịch sử chat thường xuyên. Hệ thống chỉ gửi 6 tin nhắn gần nhất để đỡ tốn token.\n"
        "2. [cyan]/model[/cyan]: Nếu dùng model 70B hay 120B sẽ rất nhanh hết token. Hãy đổi về [green]1 (Llama 3.1 8B)[/green].\n"
        "3. Chia nhỏ yêu cầu: Đừng bảo viết cả app 1000 dòng. Hãy bảo viết từng hàm một.\n"
        "4. Code ngắn gọn: Yêu cầu AI 'viết code ngắn gọn, tối giản'.",
        title="[bold red]Tối ưu Token[/bold red]",
        border_style="red"
    ))

def main():
    if not API_KEY:
        console.print("[bold red]❌ Thiếu AI_API_KEY![/bold red]")
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
                if cmd == "/help": show_banner()
                elif cmd == "/tokens": help_tokens()
                elif cmd == "/model":
                    change_model()
                    messages = [{"role": "system", "content": get_system_prompt()}]
                elif cmd == "/lang":
                    change_language()
                    messages = [{"role": "system", "content": get_system_prompt()}]
                elif cmd == "/clear":
                    messages = [{"role": "system", "content": get_system_prompt()}]
                    console.print("[yellow]Đã xóa lịch sử (Tiết kiệm token).[/yellow]")
                elif cmd == "/ls":
                    out, err, _ = execute_command("ls -la")
                    console.print(Panel(out + err, title="Files", border_style="dim"))
                elif cmd == "/cat":
                    file_name = user_input.replace("/cat", "").strip()
                    out, err, _ = execute_command(f"cat {file_name}")
                    console.print(Panel(out + err, title=f"Nội dung {file_name}", border_style="dim"))
                elif cmd == "/exec":
                    command = user_input.replace("/exec", "").strip()
                    out, err, code = execute_command(command)
                    console.print(Panel(out + err, title=f"Exit: {code}", border_style="yellow"))
                else:
                    console.print("[red]Lệnh không hợp lệ.[/red]")
                continue

            messages.append({"role": "user", "content": user_input})
            
            for step in range(10):
                with console.status(f"[bold cyan]Zuse đang code...[/bold cyan]"):
                    response = call_ai(messages)
                
                if not response: break
                
                json_res = extract_json(response)
                if not json_res:
                    console.print(f"[bold yellow]🤖 Zuse:[/bold yellow] {response}")
                    messages.append({"role": "assistant", "content": response})
                    messages.append({"role": "user", "content": "Lỗi: Chỉ trả về JSON."})
                    continue

                messages.append({"role": "assistant", "content": response})
                action = json_res.get("action")

                if action == "write":
                    path = json_res.get("path")
                    content = json_res.get("content")
                    console.print(f"[green]✍️ Ghi file:[/green] {path}")
                    with open(path, "w", encoding="utf-8") as f: f.write(content)
                    messages.append({"role": "user", "content": f"Đã ghi {path}. Chạy thử đi."})
                
                elif action == "run":
                    cmd = json_res.get("command")
                    console.print(f"[yellow]⚙️ Chạy:[/yellow] {cmd}")
                    out, err, code = execute_command(cmd)
                    output = out + err
                    if output.strip():
                        console.print(Panel(output.strip(), title="Output", border_style="dim"))
                    
                    if code == 0:
                        console.print("[green]✅ Thành công![/green]")
                        messages.append({"role": "user", "content": f"Thành công. Output: {output}"})
                    else:
                        console.print("[red]❌ Lỗi, AI tự sửa![/red]")
                        messages.append({"role": "user", "content": f"Lỗi: {output}. Sửa và chạy lại."})

                elif action == "done":
                    console.print(f"\n[bold green]🤖 Zuse:[/bold green] {json_res.get('content')}")
                    break

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
