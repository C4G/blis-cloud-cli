import click
import docker as lib_docker

@click.group()
def docker():
    pass

@click.command()
def status():
    client = lib_docker.from_env()
    click.echo("containers:")
    for c in client.containers.list():
        click.echo(c.name)
        click.echo(c.image)

docker.add_command(status)