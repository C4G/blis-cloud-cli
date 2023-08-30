import click

from util import bash
from util import packages

def install():
    click.echo("Removing old versions of Docker...")
    packages.remove(["docker", "docker-engine", "docker.io", "containerd", "runc"])

    click.echo("Installing prerequisites...")
    packages.install(["ca-certificates", "curl", "gnupg", "lsb-release"])
