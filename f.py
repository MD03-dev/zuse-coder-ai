from rich.console import Console

console = Console()

# Example data structures (you may replace these with your actual data)
AVAILABLE_MODELS = {
    "1": "Model-A",
    "2": "Model-B",
    "3": "Model-C",
}
LANGUAGES = {
    "en": "English",
    "vi": "Vietnamese",
    "es": "Spanish",
    "fr": "French",
}

CURRENT_MODEL = None
CURRENT_LANGUAGE = "en"

def change_model():
    console.print("[bold]Chọn mô hình (model):[/bold]")
    for key, name in AVAILABLE_MODELS.items():
        console.print(f"{key}. {name}")
    console.print("0. Trở lại")
    choice = console.input("Nhập lựa chọn của bạn: ")
    if choice == "0":
        return
    if choice in AVAILABLE_MODELS:
        global CURRENT_MODEL
        CURRENT_MODEL = AVAILABLE_MODELS[choice]
        console.print(f"[bold green]✅ Đã đổi sang: {CURRENT_MODEL}[/bold green]")
    else:
        console.print("[red]Không hợp lệ.[/red]")

def change_language():
    console.print("[bold]Chọn ngôn ngữ:[/bold]")
    for code, name in LANGUAGES.items():
        console.print(f"{code}: {name}")
    console.print("0. Trở lại")
    choice = console.input("Nhập mã ngôn ngữ của bạn: ")
    if choice == "0":
        return
    if choice in LANGUAGES:
        global CURRENT_LANGUAGE
        CURRENT_LANGUAGE = choice
        console.print(f"[bold green]✅ Đã đổi ngôn ngữ sang: {LANGUAGES[choice]}[/bold green]")
    else:
        console.print("[red]Không hợp lệ.[/red]")

def main_menu():
    while True:
        console.print("\n[bold]Menu chính[/bold]")
        console.print("1. Đổi mô hình")
        console.print("2. Đổi ngôn ngữ")
        console.print("0. Thoát")
        opt = console.input("Lựa chọn của bạn: ")
        if opt == "1":
            change_model()
        elif opt == "2":
            change_language()
        elif opt == "0":
            console.print("[bold]Tạm biệt![/bold]")
            break
        else:
            console.print("[red]Lựa chọn không hợp lệ.[/red]")

if __name__ == "__main__":
    main_menu()
