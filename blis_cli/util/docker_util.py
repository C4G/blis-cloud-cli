import docker
import shutil
import subprocess

from blis_cli.util import config


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
        return "docker compose"
    elif compose_v1_installed():
        return "docker-compose"
    else:
        return None


# Finds the _first_ container running the BLIS image.
def blis_container(client=None):
    try:
        client = client or docker.from_env()
        img_tag = config.compose_key("services.app.image")
        for container in client.containers.list():
            if img_tag in container.image.tags:
                return container
    except Exception as e:
        return None
    return None
