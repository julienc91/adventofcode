from collections.abc import Iterator
from typing import overload


@overload
def parse_input(type_: type[str] = str) -> Iterator[str]: ...
@overload
def parse_input[T: (int, str)](type_: type[T]) -> Iterator[T]: ...
def parse_input(type_=str):
    try:
        while True:
            yield type_(input())
    except EOFError:
        pass
