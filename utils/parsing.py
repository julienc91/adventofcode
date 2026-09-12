from collections.abc import Iterator


def parse_input[T: type[int, str]](type_: type[T] = str) -> Iterator[T]:
    try:
        while True:
            yield type_(input())
    except EOFError:
        pass
