import json
from typing import Any


def iterate(obj: Any, ignore_red: bool) -> int:
    match obj:
        case int():
            return obj
        case list():
            return sum(iterate(item, ignore_red) for item in obj)
        case dict():
            if ignore_red and ("red" in obj or "red" in obj.values()):
                return 0
            return sum(
                iterate(k, ignore_red) + iterate(v, ignore_red) for k, v in obj.items()
            )
        case _:
            return 0


def main1() -> int:
    data = json.loads(input())
    return iterate(data, ignore_red=False)


def main2() -> int:
    data = json.loads(input())
    return iterate(data, ignore_red=True)
