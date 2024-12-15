import contextlib
import importlib
import io
import sys
from collections.abc import Callable, Iterator
from pathlib import Path
from types import ModuleType


@contextlib.contextmanager
def override_stdin(stream: io.StringIO) -> Iterator[None]:
    original = sys.stdin
    sys.stdin = stream
    yield
    sys.stdin = original


def get_puzzle_module(year: int, day: int) -> ModuleType:
    file_name = f"{year:02d}.{day:02d}.{day:02d}"
    return importlib.import_module(file_name)


def get_puzzle_input(year: int, day: int) -> str:
    input_file = Path(f"inputs/{year:02d}") / Path(f"{day:02d}")
    return input_file.read_text()


def run_puzzle_func(year: int, day: int, func_name: str) -> int | str:
    module = get_puzzle_module(year, day)
    func: Callable[[], int | str] = getattr(module, func_name)
    input_data = get_puzzle_input(year, day)

    with override_stdin(io.StringIO(input_data)):
        return func()
