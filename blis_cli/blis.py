#!/usr/bin/env python3

import click
import os
import sys
import psutil

from blis_cli.util import docker_commands as blis_docker
from blis_cli.util import docker_util as blis_docker_util
from blis_cli.util import environment as blis_env
from blis_cli.util import emoji
from blis_cli.util import bash
from blis_cli.commands import install as cmd_install
from blis_cli.commands import status as cmd_status


@click.command()
def version():
    click.echo("BLIS Cloud Utility v0.0.1")


@click.command()
def status():
    exit(cmd_status.run())


@click.command()
def install():
    exit(cmd_install.install())


@click.group()
def entry_point():
    pass


def main():
    entry_point.add_command(install)
    entry_point.add_command(status)
    entry_point.add_command(version)

    entry_point.add_command(blis_docker.docker)

    entry_point()
