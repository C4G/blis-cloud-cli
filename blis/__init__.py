import click
import os
import sys
import psutil

from .docker import commands as blis_docker
from .docker import util as blis_docker_util
from .util import environment as blis_env
from .util import emoji

@click.command()
def version():
    click.echo("BLIS Cloud Utility v0.0.1")

@click.command()
def status():
    try:
        click.echo(f"Total RAM: {psutil.virtual_memory().total / (1024.**3)} GB")
        click.echo(f"Passwordless sudo: {emoji.GREEN_CHECK if blis_env.can_sudo() else emoji.RED_X}")
        click.echo(f"Docker is installed: {emoji.GREEN_CHECK if blis_docker_util.installed() else emoji.RED_X}")
        click.echo(f"Docker Compose: {blis_docker_util.compose()}")
    except:
        click.echo("There was a problem getting the status of BLIS!")
        exit(1)


@click.group()
def entry_point():
    pass

entry_point.add_command(status)
entry_point.add_command(version)

entry_point.add_command(blis_docker.docker)