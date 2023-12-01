import re

from utils.parsing import parse_input


def get_calibration(line: str) -> int:
    line = re.sub(r"\D", "", line)
    return int(line[0] + line[-1])


def main1() -> int:
    return sum(get_calibration(line) for line in parse_input())


def main2() -> int:
    def replace(line_: str) -> str:
        replacements = [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
        ]
        for number, word in enumerate(replacements, start=1):
            start, *_, finish = word
            line_ = line_.replace(word, f"{start}{number}{finish}")
        return line_

    return sum(get_calibration(replace(line)) for line in parse_input())
