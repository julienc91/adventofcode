import re

from utils.parsing import parse_input


def main1() -> int:
    res = 0
    for line in parse_input():
        for match in re.finditer(r"mul\((\d+),(\d+)\)", line):
            a, b = match.groups()
            res += int(a) * int(b)
    return res


def main2() -> int:
    res = 0
    enable = True
    for line in parse_input():
        for match in re.finditer(r"do\(\)|don\'t\(\)|mul\((\d+),(\d+)\)", line):
            if str(match.group()) == "do()":
                enable = True
            elif str(match.group()) == "don't()":
                enable = False
            elif enable:
                a, b = match.groups()[-2:]
                res += int(a) * int(b)
    return res
