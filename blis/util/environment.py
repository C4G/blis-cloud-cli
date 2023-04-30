import subprocess

def can_sudo():
    result = subprocess.run(["sudo", "-n", "echo", "hello"], capture_output=True)
    return result.returncode == 0 and result.stdout == b"hello\n"
