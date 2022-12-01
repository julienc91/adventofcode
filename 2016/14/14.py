import re
from collections.abc import Iterator
from functools import cache
from hashlib import md5


class Generator1:
    repeat_triplet_regex = re.compile(r"((\w)\2{2})")
    repeat_quintuplet_regex = re.compile(r"((\w)\2{4})")

    def __init__(self, salt: str):
        self.salt = salt
        self.index = 0
        self.__known_quintuplets: list[tuple[str, int]] = []
        self.__last_checked_quintuplet = -1

    def __iter__(self) -> Iterator[tuple[int, str]]:
        return self

    def __next__(self) -> tuple[int, str]:
        while True:
            key = self.get_hash(self.index)
            if self._is_key(key, self.index):
                self.index += 1
                return self.index - 1, key
            self.index += 1

    @cache
    def get_hash(self, index: int) -> str:
        return md5((self.salt + str(index)).encode()).hexdigest()

    def _is_key(self, key: str, index: int) -> bool:
        match = self.repeat_triplet_regex.search(key)
        if not match:
            return False
        return self._confirm_key(index, match.group(2))

    def _confirm_key(self, index: int, char: str) -> bool:
        search = char * 5
        for hash_, hash_index in self.__known_quintuplets:
            if hash_index > index + 1000:
                return False
            if hash_index <= index:
                continue

            if search in hash_:
                return True

        check_index = self.__last_checked_quintuplet + 1
        while check_index <= index + 1000:
            hash_ = self.get_hash(check_index)
            self.__last_checked_quintuplet = check_index

            if self.repeat_quintuplet_regex.search(hash_):
                self.__known_quintuplets.append((hash_, check_index))

                if search in hash_:
                    return True
            check_index += 1
        return False


class Generator2(Generator1):
    @cache
    def get_hash(self, index: int) -> str:
        res = super().get_hash(index)
        for _ in range(2016):
            res = md5(res.encode()).hexdigest()
        return res


def _main(generator_class: type[Generator1 | Generator2]) -> int:
    salt = input().strip()
    last_key_index = -1
    generator = generator_class(salt)
    for _ in range(64):
        last_key_index, _ = next(generator)
    return last_key_index


def main1() -> int:
    return _main(Generator1)


def main2() -> int:
    return _main(Generator2)
