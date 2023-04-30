import os
import subprocess

def can_sudo():
    result = subprocess.run(["sudo", "-n", "echo", "hello"], capture_output=True)
    return result.returncode == 0 and result.stdout == b"hello\n"

def distro():
    result = subprocess.run(["grep", "DISTRIB_CODENAME", "/etc/lsb-release"], capture_output=True)
    if result.returncode == 0:
        return result.stdout.decode('utf-8').strip().split("=")[1]
    else:
        return None