import click

from api import aoc_client
from api.exceptions import AuthenticationException, NotLoggedInException

from .cli import cli


@cli.group()
def auth() -> None:
    pass


@auth.command()
def check() -> None:
    try:
        _ = aoc_client.check_auth()
    except (AuthenticationException, NotLoggedInException):
        raise click.ClickException("Authentication failed")
    click.echo("Authentication successful")


@auth.command()
def login() -> None:
    cookie = click.prompt("Enter your AOC cookie", hide_input=True)
    if not cookie:
        raise click.ClickException("Invalid cookie")

    try:
        aoc_client.set_cookie(cookie)
    except AuthenticationException:
        raise click.ClickException("Authentication failed")


@auth.command()
def logout() -> None:
    aoc_client.unset_cookie()
