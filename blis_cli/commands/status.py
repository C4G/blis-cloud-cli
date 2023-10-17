import click
import psutil

from blis_cli.util import config
from blis_cli.util import emoji
from blis_cli.util import environment as blis_env
from blis_cli.util import docker_util as blis_docker_util

def run():
    try:
        if blis_docker_util.blis_container() != None:
            click.secho("BLIS is running!", fg="green", nl=False)
            click.echo(f" ({config.compose_key('services.app.image')})")
        else:
            click.secho("BLIS is NOT running!", fg="yellow")
        click.echo("----------------")

        click.echo(
            f"Total RAM: {psutil.virtual_memory().total / (1024.**3)} GiB")
        click.echo(
            f"Supported distribution: {emoji.GREEN_CHECK if blis_env.supported_distro() else emoji.RED_X} ({blis_env.distro()})")
        click.echo(
            f"Passwordless sudo: {emoji.GREEN_CHECK if blis_env.can_sudo() else emoji.RED_X}")
        click.echo(
            f"Docker is installed: {emoji.GREEN_CHECK if blis_docker_util.installed() else emoji.RED_X}")
        click.echo(f"Docker Compose: {emoji.GREEN_CHECK if blis_docker_util.compose() is not None else emoji.RED_X}")
        click.echo(
            f"User '{blis_env.user()}' in 'docker' group: {emoji.GREEN_CHECK if blis_env.in_docker_grp() else emoji.RED_X}")
        return 0
    except Exception as e:
        click.echo("There was a problem getting the status of BLIS!")
        click.echo(e)
        return 1
