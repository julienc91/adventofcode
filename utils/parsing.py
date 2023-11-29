from collections.abc import Iterator


def parse_input() -> Iterator[str]:
    try:
        while True:
            yield input()
    except EOFError:
        pass
