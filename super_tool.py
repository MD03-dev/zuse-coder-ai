import sys
import time
import platform
import shutil

# Check if termux-tools is installed for clearing screen
try:
    import termux
    def clear():
        termux.clear()
except ImportError:
    def clear():
        os.system('clear' if sys.platform != 'win32' else 'cls')

def banner():
    clear()
    print("\033[1;36m")
    print("+======================================+")
    print("|        ZUSE SUPER SYST              |")
    print("|       Terminal Utility Tool         |")
    print("+======================================+")
    print("\033[0m", end="")

def option1_sysinfo():
    info = {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor()
    }
    print("\033[1;33m[ SYS INFO ]\033[0m")
    for key, value in info.items():
        print(f"  {key}: {value}")

def option2_disk():
    print("\n\033[1;33m[ DISK USAGE ]\033[0m")
    usage = shutil.disk_usage(".")
    total = usage.total / (1024 ** 3)
    used = usage.used / (1024 ** 3)
    free = usage.free / (1024 ** 3)
    print(f"  Total: {total:.2f} GB")
    print(f"  Used:  {used:.2f} GB")
    print(f"  Free:  {free:.2f} GB")

def option3_network_check():
    print("\n\033[1;33m[ NETWORK CHECK ]\033[0m")
    try:
        import subprocess
        subprocess.run(["ping", "-c", "2", "google.com"], check=True, stdout=subprocess.DEVNULL)
        print("\033[1;32m[ OK ]\033[0m Internet connection is active.")
    except Exception:
        print("\033[1;31m[FAIL]\033[0m Internet connection failed or ping unavailable.")

def main():
    banner()
    print("\033[1;37m\033[0m")
    print(" [1] System Info")
    print(" [2] Disk Usage")
    print(" [3] Network Check")
    print(" [0] Exit")
    
    while True:
        try:
            choice = input("\n Select option: ").strip()
            if choice == '1':
                option1_sysinfo()
            elif choice == '2':
                option2_disk()
            elif choice == '3':
                option3_network_check()
            elif choice == '0':
                print("\033[1;36mThanks for using ZUSE Super System.\033[0m")
                time.sleep(2)
                break
            else:
                print("Invalid selection.")
        except (KeyboardInterrupt, EOFError):
            print("\n\033[1;31m[ INFO ]\033[0m Interrupted by user. Goodbye!")
            break

if __name__ == "__main__":
    main()
