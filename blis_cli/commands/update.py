import click
import docker

from blis_cli.util import bash
from blis_cli.util import config
from blis_cli.util import emoji
from blis_cli.util import docker_util

def run():
    restart_blis = False
    if docker_util.blis_container() is not None:
        click.secho("BLIS must be stopped in order to update to the latest version.", fg="yellow")
        if not click.confirm("Continue stopping BLIS?"):
            return 0
        click.echo("Stopping BLIS... ", nl=False)
        docker_util.blis_container().stop()
        click.secho("Success!", fg="green")
        restart_blis = True

    click.echo("Updating BLIS... ", nl=False)
    out, err = bash.run(
        f"{docker_util.compose()} -f {config.compose_file()} pull app"
    )
    if err:
        click.secho("Failed", fg="red")
        click.echo(err, err=True)
        return 1
    click.secho("Success!", fg="green")

    if restart_blis:
        click.echo("Starting BLIS... ", nl=False)
        out, err = bash.run(
            f"{docker_util.compose()} -f {config.compose_file()} up -d --wait app"
        )
        if err:
            click.secho("Failed", fg="red")
            click.echo(err, err=True)
            return 1

        click.secho("Success!", fg="green")
        return 0

    return 0
