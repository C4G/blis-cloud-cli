import click
import psutil
import socket

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

    domains = caddy.get_domains()
    if len(domains) < 1:
        click.echo("\nThere are no domains configured. Please run:")
        click.echo("  blis domain add [mydomain.example.com]")
        exit(0)

    # These are only "possible" IPs because the computer
    # might be behind a firewall/NAT and these will only contain
    # the local IP addresses.
    possible_ipv4_addrs = get_interfaces()

    for domain in domains:
        click.echo()
        click.secho(domain, fg="green")
        click.echo("IP Addresses: ", nl=False)
        ip_addrs = get_ipv4_by_hostname(domain)
        click.secho(", ".join(ip_addrs), fg="green")

        for ip in ip_addrs:
            if ip in possible_ipv4_addrs:
                click.secho("Domain points to computer!")
                break

    exit(0)


@click.command()
@click.argument("name")
def add(name: str):
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

    current_domains = caddy.get_domains()
    current_domains.append(name)
    caddy.set_domains(current_domains)


@click.command()
def clear():
    caddy.set_domains([])


entrypoint.add_command(add)
entrypoint.add_command(clear)
entrypoint.add_command(status)


# Source:
# https://stackoverflow.com/questions/2805231/how-can-i-do-dns-lookups-in-python-including-referring-to-etc-hosts/66000439#66000439
def get_ipv4_by_hostname(hostname):
    # see `man getent` `/ hosts `
    # see `man getaddrinfo`
    try:
        return list(
            i[4][0]  # raw socket structure  # internet protocol info  # address
            for i in socket.getaddrinfo(hostname, 0)  # port, required
            if i[0] is socket.AddressFamily.AF_INET  # ipv4
            # ignore duplicate addresses with other socket types
            and i[1] is socket.SocketKind.SOCK_RAW
        )
    except Exception as e:
        click.secho(str(e), fg="red", nl=False)
        return []


def get_interfaces():
    addrs = psutil.net_if_addrs()
    ip_addrs = []
    for key in addrs:
        addr = addrs[key]
        for a in addr:
            if a.family == socket.AddressFamily.AF_INET:
                ip_addrs.append(a.address)

    return ip_addrs

