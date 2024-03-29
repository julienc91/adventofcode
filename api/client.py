import os
from pathlib import Path

import appdirs
import httpx
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
        self.check_auth({"session": cookie})

        self.CACHE_DIRECTORY.mkdir(parents=True, exist_ok=True)
        self.CACHE_FILE.write_text(cookie)

    def unset_cookie(self) -> None:
        try:
            os.remove(self.CACHE_FILE)
        except FileNotFoundError:
            pass

    def check_auth(self, cookies: dict[str, str] | None = None) -> None:
        response = httpx.get(f"{self.BASE_URL}/", cookies=cookies or self._cookies)
        if response.status_code != 200:
            raise AuthenticationException()

        page = BeautifulSoup(response.content, features="html.parser")
        username_container = page.select("header .user")
        if not username_container:
            raise AuthenticationException()

    def get_text(self, path: str) -> str:
        response = httpx.get(
            f"{self.BASE_URL}/{path.lstrip('/')}", cookies=self._cookies
        )
        if response.status_code != 200:
            raise AuthenticationException()
        return response.text

    def post_html(self, path: str, data: dict[str, str]) -> BeautifulSoup:
        response = httpx.post(
            f"{self.BASE_URL}/{path.lstrip('/')}", cookies=self._cookies, data=data
        )
        if response.status_code != 200:
            raise AuthenticationException()

        page = BeautifulSoup(response.content, features="html.parser")
        username_container = page.select("header .user")[0]
        if not username_container:
            raise AuthenticationException()
        return page


aoc_client = AOCClient()
