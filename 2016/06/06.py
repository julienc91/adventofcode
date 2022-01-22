from collections import Counter
from typing import Callable


def parse_messages() -> list[str]:
    res: list[str] = []
    try:
        while line := input().strip():
            res.append(line)
    except EOFError:
        pass
    return res


def _main(selector: Callable[[Counter[str]], str]) -> str:
    messages = parse_messages()
    message_length = len(messages[0])
    res = ""
    for i in range(message_length):
        chars_on_column = Counter([message[i] for message in messages])
        res += selector(chars_on_column)
    return res


def main1() -> str:
    return _main(lambda c: c.most_common()[0][0])


def main2() -> str:
    return _main(lambda c: c.most_common()[-1][0])
