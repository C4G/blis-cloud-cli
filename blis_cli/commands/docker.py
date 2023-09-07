import click
import docker

from blis_cli.util import environment as env
from blis_cli.util import packages


@click.group()
def entrypoint():
    pass


@click.command
def purge():
    if not env.can_sudo():
        click.secho("You must have root privileges to run this.", fg="red")
        exit(1)
    
    packages.remove(["docker", "docker-engine", "docker.io", "containerd", "runc"])
    packages.remove(
        [
            "docker-ce",
            "docker-ce-cli",
            "containerd.io",
            "docker-compose-plugin",
            "docker-buildx-plugin",
        ]
    )
    packages.apt_update()


@click.command
def status():
    client = docker.from_env()
    click.echo("containers:")
    for c in client.containers.list():
        click.echo(c.name)
        click.echo(c.image)


entrypoint.add_command(purge)
entrypoint.add_command(status)
