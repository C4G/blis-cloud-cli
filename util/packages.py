import click

from util import bash


def apt_update():
    click.echo("Running apt-get update...")
    out, err = bash.sudo("DEBIAN_FRONTEND=noninteractive apt-get update")
    if err == None:
        click.echo(" => Success!")
    else:
        click.echo(" => Failure!")
        click.echo(err)


def install(packages: list):
    click.echo(f"Installing packages: {packages}")
    out, err = bash.sudo(
        f"DEBIAN_FRONTEND=noninteractive apt-get install -y {' '.join(packages)}")
    if err == None:
        click.echo(" => Success!")
    else:
        click.echo(" => Failure!")
        click.echo(err)


def remove(packages: list):
    click.echo(f"Removing packages: {packages}")
    out, err = bash.sudo(
        f"DEBIAN_FRONTEND=noninteractive apt-get remove -y {' '.join(packages)}")
    if err == None:
        click.echo(" => Success!")
    else:
        click.echo(" => Failure!")
        click.echo(err)


def is_installed(package: str):
    _, err = bash.run(f"dpkg -s {package}")
    return err == None
