import click
import os
import yaml


def basedir():
    return os.path.expanduser("~/.blis")


def make_basedir():
    if not os.path.exists(basedir()):
        os.makedirs(basedir())


def config_file():
    return os.path.join(basedir(), "blis-cloud-config.yml")


def compose_file():
    return os.path.join(basedir(), "docker-compose.yml")


def validate_compose():
    dcmp = {}
    with open(compose_file(), "r") as f:
        try:
            dcmp = yaml.safe_load(f)
        except yaml.YAMLError as e:
            click.echo(e, err=True)
            return False

    if 'name' not in dcmp:
        click.echo("Missing 'name' in docker-compose.yml", err=True)
        return False
    
    return True
