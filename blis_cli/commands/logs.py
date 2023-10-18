import click
import docker
import tarfile
import tempfile

from blis_cli.util import config
from blis_cli.util import emoji
from blis_cli.util import environment
from blis_cli.util import docker_util

def run():
    try:
        c = docker_util.blis_container()

        # This is technically not required. We could probably extract logs from
        # a stopped BLIS since the /log folder is mounted as its own volume.
        # However... I don't know how to reliably do that right now.
        # And it would definitely need root.
        if c == None:
            click.secho("BLIS is not running.", fg="red")
            click.echo("Please start BLIS to see logs.")
            return 0

        with tempfile.TemporaryFile() as f:
            # bits, stat = c.get_archive('/var/log/apache2/error.log')
            bits, stat = c.get_archive('/var/www/blis/log/application.log')

            for chunk in bits:
                f.write(chunk)

            f.seek(0)
            tf = tarfile.open(fileobj=f)
            m = tf.extractfile("application.log")
            for chunk in m:
                click.echo(chunk, nl=False)

    except docker.errors.NotFound as e:
        click.echo("The log file was not found.")
        return 1
    except Exception as e:
        click.echo(e.__class__)
        click.echo("There was a problem getting the logs for BLIS!")
        click.echo(e)
        return 1
