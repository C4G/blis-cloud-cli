import click
import os
import docker as lib_docker
import shutil

from blis_cli.util import bash
from blis_cli.util import config
from blis_cli.util import docker_util as docker
from blis_cli.util import emoji
from blis_cli.util import environment as env
from blis_cli.util import packages


def install():
    if not docker.installed():
        click.secho("You must install Docker before continuing. Please run:", fg="red")
        click.echo("  sudo blis docker install")
        return 1

    if not env.in_docker_grp():
        click.secho("You must be in the Docker group to continue. Please run", fg="red")
        click.echo("  sudo blis docker install")
        return 1

    # We have Docker installed and we are in the docker group.
    version = lib_docker.from_env().version()
    click.echo(f"Docker version: {click.style(version['Version'], fg='green')}")

    if not click.confirm(
        "BLIS has already been installed in ~/.blis. Do you want to overwrite the configuration?"
    ):
        return 0

    config.make_basedir()
    copy_docker_files()

    if config.validate_compose():
        click.echo("docker-compose.yml is valid.")
    else:
        click.secho("docker-compose.yml is not valid.", fg="red")
        return 1

    run_blis_and_setup_db()

    click.secho("You are ready to rock!", fg="green")


def copy_docker_files():
    click.echo("Copying docker-compose.yml to ~/.blis/...")
    shutil.copy(
        f"{os.path.dirname(__file__)}/../extra/docker-compose.yml",
        config.compose_file(),
    )


def run_blis_and_setup_db():
    click.echo("Starting BLIS for the first time... ", nl=False)
    out, err = bash.run(f"{docker.compose()} -f {config.compose_file()} up -d")
    if err:
        click.secho("Failed", fg="red")
        click.echo(err, err=True)
        return False

    # TODO: setup db

    out, err = bash.run(f"{docker.compose()} -f {config.compose_file()} down")
    if err:
        click.secho("Failed", fg="red")
        click.echo(err, err=True)
        return False

    click.secho("Success!", fg="green")
