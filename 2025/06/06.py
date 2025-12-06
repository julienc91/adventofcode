import math
import re

from utils.parsing import parse_input


def main1() -> int:
    first_line = input()
    numbers = map(int, re.findall(r"\d+", first_line))
    res = 0
    problems = [[number] for number in numbers]

    for line in parse_input():
        if line.startswith(("+", "*")):
            for i, operator in enumerate(re.findall(r"[+*]", line)):
                if operator == "+":
                    res += sum(problems[i])
                elif operator == "*":
                    res += math.prod(problems[i])
        else:
            for i, number in enumerate(map(int, re.findall(r"\d+", line))):
                problems[i].append(number)
    return res


def main2() -> int:
    text = list(parse_input())
    line_length = max(len(line) for line in text)
    res = 0

    operator = None
    numbers = []
    for x in range(line_length):
        number = ""
        for y in range(len(text)):
            if x >= len(text[y]):
                continue

            if text[y][x].isdigit():
                number += text[y][x]
            elif text[y][x] == "+":
                operator = sum
            elif text[y][x] == "*":
                operator = math.prod

        if number:
            numbers.append(int(number))

        if not number or x == line_length - 1:
            assert operator
            res += operator(numbers)
            numbers = []
            operator = None

    return res
