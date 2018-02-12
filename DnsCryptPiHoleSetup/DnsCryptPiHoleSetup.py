from DnsCryptPiHoleSetup.DefaultConfig import host, password, user

import click

from DnsCryptPiHoleSetup.ClickConfig import install, setDefaultConfig
from DnsCryptPiHoleSetup.ClickHelperClasses import ShowDefaultSingleQuote
from click_help_colors import HelpColorsCommand


@click.command(cls=click.CommandCollection,
               sources=[install, setDefaultConfig])
@click.command(context_settings=dict(max_content_width=500),
               cls=HelpColorsCommand, help_options_color='blue', help_headers_color='yellow')
@click.option('--host', '-h', default=host, help='Host or IP address that the Dnscrypt proxy script will ran against',
              show_default=True, cls=ShowDefaultSingleQuote)
@click.option('--user', '-u', default=user, help='Username for host that the Dnscrypt proxy script will ran against',
              show_default=True, cls=ShowDefaultSingleQuote)
@click.option('--password', '-p', default=password,
              help='Password for host that the Dnscrypt proxy script will ran against', show_default=True,
              cls=ShowDefaultSingleQuote)
def cli(host, user, password):
    pass


if __name__ == '__main__':
    cli()
