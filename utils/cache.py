import json
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")


@contextmanager
def pre_compute(
    builder: Callable[[], T], year: int, puzzle_id: int, cache_id: str = ""
) -> Iterator[T]:
    cache_directory = Path(f"{year}") / Path(f"{puzzle_id:02d}")
    cache_filename = f".{cache_id or 'cache'}.json"

    cache_file = cache_directory / cache_filename
    if cache_file.exists():
        cached_json = cache_file.read_text()
        cached_data = json.loads(cached_json)
        yield cached_data
    else:
        cached_data = builder()
        yield cached_data

        cache_file.write_text(json.dumps(cached_data, indent=True))
