import click

from blis_cli.util import caddy
from blis_cli.util import docker_util


@click.group()
def entrypoint():
    pass


@click.command()
def status():
    click.secho("Caddy is configured: ", nl=False)
    if caddy.installed():
        click.secho("Yes!", fg="green")
    else:
        click.secho("No", fg="red")
        click.echo("\nThere are no domains configured. Please run:")
        click.echo("  blis domain add [mydomain.example.com]")
        exit(0)
    exit(0)


@click.command()
@click.argument("name")
@click.option(
    "--no-verify", default=False, is_flag=True, help="Skip domain verification."
)
def add(name: str, no_verify: bool):
    click.secho(f"Adding {name} to Caddyfile", fg="green")
    click.confirm("Do you want to proceed?", abort=True)

    restart_blis = False
    if docker_util.blis_container() is not None:
        click.secho(
            "BLIS must be stopped in order to update to the latest version.",
            fg="yellow",
        )
        if not click.confirm("Continue stopping BLIS?"):
            return 0
        click.echo("Stopping BLIS... ", nl=False)
        docker_util.blis_container().stop()
        click.secho("Success!", fg="green")
        restart_blis = True

    caddy.install()

    caddy.set_domains([name])


@click.command()
def remove():
    caddy.set_domains([])


entrypoint.add_command(add)
entrypoint.add_command(remove)
entrypoint.add_command(status)


def verify_domain(name):
    domain_ips = get_ipv4_by_hostname(name)
    return len(domain_ips) > 0


# Source:
# https://stackoverflow.com/questions/2805231/how-can-i-do-dns-lookups-in-python-including-referring-to-etc-hosts/66000439#66000439
def get_ipv4_by_hostname(hostname):
    # see `man getent` `/ hosts `
    # see `man getaddrinfo`

    return list(
        i[4][0]  # raw socket structure  # internet protocol info  # address
        for i in socket.getaddrinfo(hostname, 0)  # port, required
        if i[0] is socket.AddressFamily.AF_INET  # ipv4
        # ignore duplicate addresses with other socket types
        and i[1] is socket.SocketKind.SOCK_RAW
    )
