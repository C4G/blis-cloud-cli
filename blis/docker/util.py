import shutil
import subprocess

def installed():
    return shutil.which("docker") is not None

def compose_v1_installed():
    if not installed():
        return False
    return shutil.which("docker-compose") is not None

def compose_v2_installed():
    if not installed():
        return False
    res = subprocess.run(["docker", "compose"], capture_output=True)
    return res.returncode == 0

def compose():
    if compose_v2_installed():
        return "docker", "compose"
    elif compose_v1_installed():
        return "docker-compose"
    else:
        raise Exception("Docker Compose is not installed.")