import click
import psutil

from blis_cli.util import config
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

        total_ram = psutil.virtual_memory().total / (1024.0**3)
        click.echo(f"Total RAM: {total_ram:.2f} GiB")
        if total_ram < 0.9:
            click.secho(
                "1GB of RAM is recommended to run BLIS. Things might not work as expected!",
                fg="red",
            )

        click.echo("Supported distribution: ", nl=False)
        if blis_env.supported_distro():
            click.secho("Yes!", fg="green")
        else:
            click.secho("No", fg="red")
            click.echo("BLIS is supported on these Ubuntu distributions: ", nl=False)
            click.secho(", ".join(blis_env.SUPPORTED_DISTROS), fg="green")
            click.echo("You have: ", nl=False)
            click.secho(blis_env.distro(), fg="green")

        click.echo("Passwordless sudo: ", nl=False)
        if blis_env.can_sudo():
            click.secho("Yes!", fg="green")
        else:
            click.secho("No", fg="red")

        if (
            blis_docker_util.blis_container() == None
            and not blis_docker_util.installed()
        ):
            click.secho(
                "Please run `blis docker status` to check the status of Docker on your machine.",
                fg="yellow",
            )

        return 0
    except Exception as e:
        click.echo("There was a problem getting the status of BLIS!")
        click.echo(e)
        return 1
