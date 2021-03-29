import db
import webserver
from werkzeug.serving import run_simple
import os
import click


@click.group()
def cli():
    pass


ADMIN_SQL_DIR = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'admin', 'sql')


@cli.command(name="run_server")
@click.option("--host", "-h", default="0.0.0.0", show_default=True)
@click.option("--port", "-p", default=8080, show_default=True)
@click.option("--debug", "-d", is_flag=True,
              help="Turns debugging mode on or off. If specified, overrides "
                   "'DEBUG' value in the config file.")
def runserver(host, port, debug=False):
    application = webserver.create_app()
    run_simple(
        hostname=host,
        port=port,
        application=application,
        use_debugger=debug,
        use_reloader=debug,
    )

if __name__ == '__main__':
    cli()
