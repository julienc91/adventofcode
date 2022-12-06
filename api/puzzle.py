from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import AOCClient


class Puzzle:
    def __init__(self, client: "AOCClient") -> None:
        self._client = client

    def get_input(self, year: int, day: int) -> str:
        path = f"/{year}/day/{day}/input"
        return self._client.get_text(path)
