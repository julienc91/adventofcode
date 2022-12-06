import click

from api import aoc_client
from api.exceptions import AuthenticationException

from .cli import cli


@cli.group()
def auth() -> None:
    pass


@auth.command()
def login() -> None:
    cookie = click.prompt("Enter your AOC cookie", hide_input=True)
    if not cookie:
        raise click.ClickException("Invalid cookie")

    try:
        aoc_client.set_cookie(cookie)
    except AuthenticationException:
        raise click.ClickException("Authentication failed")
