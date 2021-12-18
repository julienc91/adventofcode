import re
from typing import Iterator


def parse_input() -> Iterator[str]:
    try:
        while line := input().strip():
            yield line
    except EOFError:
        pass


def main1() -> int:
    total_real_length = 0
    total_code_length = 0
    for line in parse_input():
        total_real_length += len(line)
        line = line[1:-1]
        line = line.replace("\\\\", "\\")
        line = line.replace('\\"', '"')
        line = re.sub(r"\\x[a-f0-9]{2}", "1", line)
        total_code_length += len(line)
    return total_real_length - total_code_length


def main2() -> int:
    total_real_length = 0
    total_encoded_length = 0
    for line in parse_input():
        total_real_length += len(line)
        new_line = '"'
        for c in line:
            if c == "\\" or c == '"':
                new_line += "\\"
            new_line += c
        new_line += '"'
        total_encoded_length += len(new_line)
    return total_encoded_length - total_real_length
