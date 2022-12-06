from datetime import date
from pathlib import Path

import click

from api import aoc_client

from .cli import cli
from .utils.puzzle import run_puzzle_func


@cli.group()
def puzzle() -> None:
    pass


def validate_date(day: int | None, year: int | None) -> date:
    today = date.today()
    if day is None:
        day = today.day
    elif not 1 <= day <= 25:
        raise click.BadParameter("Invalid day")

    if year is None:
        year = today.year
    elif not 2015 <= year <= today.year:
        raise click.BadParameter("Invalid year")

    if year == today.year and day > today.day:
        raise click.BadParameter("Invalid day")
    return date(year, 12, day)


@puzzle.command()
@click.option("--day", default=None, type=int)
@click.option("--year", default=None, type=int)
def run(day: int | None, year: int | None) -> None:
    puzzle_date = validate_date(day, year)

    result = run_puzzle_func(puzzle_date.year, puzzle_date.day, "main1")
    click.echo(f"main1: {result}")

    result = run_puzzle_func(puzzle_date.year, puzzle_date.day, "main2")
    click.echo(f"main2: {result}")


@puzzle.command()
@click.option("--day", default=None, type=int)
@click.option("--year", default=None, type=int)
def init(day: int | None, year: int | None) -> None:
    puzzle_date = validate_date(day, year)
    directory = Path(str(puzzle_date.year)) / f"{puzzle_date.day:02d}"

    if directory.exists():
        raise click.ClickException("Directory already exists")

    directory.mkdir(parents=True, exist_ok=False)
    try:
        input_data = aoc_client.puzzle.get_input(puzzle_date.year, puzzle_date.day)
        (directory / "input").write_text(input_data)
        (directory / f"{puzzle_date.day:02d}.py").write_text(PUZZLE_TEMPLATE)
    except Exception:
        directory.rmdir()
        raise


PUZZLE_TEMPLATE = """def main1() -> int:
    pass


def main2() -> int:
    pass
"""
