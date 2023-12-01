from typing import TypeVar
from collections.abc import Iterator


T = TypeVar("T")


def parse_input(type_: type[T] = str) -> Iterator[T]:
    try:
        while True:
            yield type_(input())
    except EOFError:
        pass
