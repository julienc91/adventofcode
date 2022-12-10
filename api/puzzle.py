from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import AOCClient


class Puzzle:
    def __init__(self, client: "AOCClient") -> None:
        self._client = client

    def get_input(self, year: int, day: int) -> str:
        path = f"/{year}/day/{day}/input"
        return self._client.get_text(path)

    def submit(
        self, year: int, day: int, level: int, answer: str | int
    ) -> tuple[bool, str]:
        path = f"/{year}/day/{day}/answer"
        data = {"level": str(level), "answer": str(answer)}
        response = self._client.post_html(path, data=data)
        text = response.select("main article")[0].text
        return "That's the right answer" in text, text
