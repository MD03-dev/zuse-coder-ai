import subprocess
def execute_command(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return res.stdout, res.stderr, res.returncode
    except Exception as e:
        return "", str(e), 1
