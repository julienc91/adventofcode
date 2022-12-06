from pathlib import Path

import appdirs
import requests
from bs4 import BeautifulSoup

from .exceptions import AuthenticationException, NotLoggedInException
from .puzzle import Puzzle


class AOCClient:
    BASE_URL = "https://adventofcode.com"
    CACHE_DIRECTORY = Path(appdirs.user_cache_dir("adventofcode"))
    CACHE_FILE = CACHE_DIRECTORY / "cookie.txt"

    @property
    def puzzle(self) -> "Puzzle":
        return Puzzle(self)

    @property
    def _cookies(self) -> dict[str, str]:
        try:
            data = self.CACHE_FILE.read_text()
        except FileNotFoundError:
            raise NotLoggedInException
        return {"session": data}

    def set_cookie(self, cookie: str) -> None:
        self.get_html("/", {"session": cookie})

        self.CACHE_DIRECTORY.mkdir(parents=True, exist_ok=True)
        self.CACHE_FILE.write_text(cookie)

    def get_html(
        self, path: str, cookies: dict[str, str] | None = None
    ) -> BeautifulSoup:
        response = requests.get(
            f"{self.BASE_URL}/{path.lstrip('/')}", cookies=cookies or self._cookies
        )
        if response.status_code != 200:
            raise AuthenticationException()

        page = BeautifulSoup(response.content, features="html.parser")
        username_container = page.select("header .user")[0]
        if not username_container:
            raise AuthenticationException()
        return page

    def get_text(self, path: str) -> str:
        response = requests.get(
            f"{self.BASE_URL}/{path.lstrip('/')}", cookies=self._cookies
        )
        if response.status_code != 200:
            raise AuthenticationException()
        return response.text


aoc_client = AOCClient()
