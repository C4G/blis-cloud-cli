from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import shutil
import subprocess
import yaml

from blis_cli.util import config


jinja2 = Environment(
    loader=FileSystemLoader(f"{os.path.dirname(__file__)}/../extra/templates/"),
    autoescape=select_autoescape()
)

def caddyfile():
    return os.path.join(config.basedir(), "Caddyfile")


def installed():
    caddyfile_exists = os.path.exists(caddyfile())
    caddy_stanza_present = config.compose_key("services.caddy")
    return caddyfile_exists and (caddy_stanza_present is not None)


def install():
    config.add_volume("caddy_data")
    config.add_volume("caddy_config")
    config.add_section_from_template("services.caddy")
    config.remove_key("services.app.ports")
    config.set_key("services.app.depends_on", ["db", "caddy"])


def set_domains(domains: list):
    template = jinja2.get_template("Caddyfile.j2")
    rendered = template.render(domains=domains)

    try:
        with open(os.path.join(config.basedir(), "Caddyfile"), "w") as f:
            f.write(rendered)
            return None
    except Exception as e:
        return e
