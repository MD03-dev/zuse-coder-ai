#!/usr/bin/env python3
import os, sys, json, requests, re, time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from tools.executor import execute_command

console = Console()
API_KEY = os.getenv("AI_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

AVAILABLE_MODELS = {
    "1": "qwen/qwen3.8-27b",
    "2": "openai/gpt-oss-120b",
    "3": "openai/gpt-oss-20b",
    "4": "allam-2-7b"
}
CURRENT_MODEL = "qwen/qwen3.8-27b"
LANGUAGES = {"1": "Vietnamese", "2": "English", "3": "Chinese"}
CURRENT_LANG = "Vietnamese"

def get_system_prompt():
    return f"""Bạn là Zuse, AI Coder Termux. Ngôn ngữ: {CURRENT_LANG}.
Quy tắc TỐI THƯỢNG: KHÔNG giải thích. CHỈ TRẢ VỀ DUY NHẤT 1 OBJECT JSON.
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
[bold green]ZUSE CODER AI v6.9.7 - Ultimate Version[/bold green]
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
    console.print(t1)
    console.print("[dim]Gõ câu lệnh thường để AI viết code.[/dim]\n")

def trim_history(messages):
    if len(messages) > 7: return [messages[0]] + messages[-6:]
    return messages

def call_ai(messages):
    global CURRENT_MODEL
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": CURRENT_MODEL, "messages": trim_history(messages)}
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        data = r.json()
        if 'error' in data:
            err_msg = data['error'].get('message', '')
            if 'Rate limit' in err_msg or 'Request too large' in err_msg:
                console.print(f"[bold red]❌ Hết Token! Gõ /model chọn số khác hoặc /clear.[/bold red]")
            elif 'does not exist' in err_msg:
                console.print(f"[bold red]❌ Model lỗi. Gõ /model chọn số khác![/bold red]")
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
    console.print("\n[bold cyan]DANH SÁCH MODEL ĐANG HOẠT ĐỘNG:[/bold cyan]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("STT", width=5)
    table.add_column("Tên Model", style="green")
    for k, v in AVAILABLE_MODELS.items(): table.add_row(k, v)
    console.print(table)
    choice = Prompt.ask("[bold green]Chọn số thứ tự (0 để hủy)[/bold green]")
    if choice in AVAILABLE_MODELS:
        CURRENT_MODEL = AVAILABLE_MODELS[choice]
        console.print(f"[bold green]✅ Đã đổi sang: {CURRENT_MODEL}[/bold green]")
    elif choice != "0": console.print("[red]Không hợp lệ.[/red]")

def change_language():
    global CURRENT_LANG
    console.print("\n[bold cyan]CHỌN NGÔN NGỮ:[/bold cyan]")
    for k, v in LANGUAGES.items(): console.print(f"[{k}] {v}")
    choice = Prompt.ask("[bold green]Chọn (1-3)[/bold green]")
    if choice in LANGUAGES:
        CURRENT_LANG = LANGUAGES[choice]
        console.print(f"[bold green]✅ Đã đổi sang: {CURRENT_LANG}[/bold green]")

def main():
    if not API_KEY:
        console.print("[bold red]❌ Thiếu AI_API_KEY![/bold red]"); sys.exit(1)
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
                elif cmd == "/model":
                    change_model(); messages = [{"role": "system", "content": get_system_prompt()}]
                elif cmd == "/lang":
                    change_language(); messages = [{"role": "system", "content": get_system_prompt()}]
                elif cmd == "/clear":
                    messages = [{"role": "system", "content": get_system_prompt()}]
                    console.print("[yellow]Đã xóa lịch sử.[/yellow]")
                else: console.print("[red]Lệnh không hợp lệ.[/red]")
                continue
            messages.append({"role": "user", "content": user_input})
            for step in range(5):
                with console.status(f"[bold cyan]Zuse đang code...[/bold cyan]"):
                    response = call_ai(messages)
                if not response: break
                json_res = extract_json(response)
                if not json_res:
                    console.print(f"[bold yellow]🤖 Zuse:[/bold yellow] {response}")
                    messages.append({"role": "assistant", "content": response})
                    messages.append({"role": "user", "content": "Lỗi: CHỈ TRẢ VỀ JSON."})
                    continue
                messages.append({"role": "assistant", "content": response})
                action = json_res.get("action")
                if action == "write":
                    path = json_res.get("path"); content = json_res.get("content")
                    console.print(f"[green]✍️ Ghi file:[/green] {path}")
                    with open(path, "w", encoding="utf-8") as f: f.write(content)
                    messages.append({"role": "user", "content": f"Đã ghi {path}. Chạy thử đi."})
                elif action == "run":
                    cmd = json_res.get("command")
                    console.print(f"[yellow]⚙️ Chạy:[/yellow] {cmd}")
                    out, err, code = execute_command(cmd)
                    output = out + err
                    if output.strip(): console.print(Panel(output.strip(), title="Output", border_style="dim"))
                    if code == 0:
                        console.print("[green]✅ Thành công![/green]")
                        messages.append({"role": "user", "content": f"Thành công. Output: {output}"})
                    else:
                        console.print("[red]❌ Lỗi, AI tự sửa![/red]")
                        messages.append({"role": "user", "content": f"Lỗi: {output}. Sửa và chạy lại."})
                elif action == "done":
                    console.print(f"\n[bold green]🤖 Zuse:[/bold green] {json_res.get('content')}")
                    break
        except KeyboardInterrupt: break

if __name__ == "__main__": main()
