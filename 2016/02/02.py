from utils.parsing import parse_input


def _main(keypad: dict[str, dict[str, str]]) -> str:
    digit = "5"
    code = ""
    for digit_instruction in parse_input():
        for direction in digit_instruction:
            digit = keypad[digit].get(direction, digit)
        code += digit
    return code


def main1() -> str:
    keypad = {
        "1": {"R": "2", "D": "4"},
        "2": {"R": "3", "D": "5", "L": "1"},
        "3": {"D": "6", "L": "2"},
        "4": {"R": "5", "D": "7", "U": "1"},
        "5": {"R": "6", "D": "8", "L": "4", "U": "2"},
        "6": {"D": "9", "L": "5", "U": "3"},
        "7": {"R": "8", "U": "4"},
        "8": {"R": "9", "L": "7", "U": "5"},
        "9": {"L": "8", "U": "6"},
    }
    return _main(keypad)


def main2() -> str:
    keypad = {
        "1": {"D": "3"},
        "2": {"R": "3", "D": "6"},
        "3": {"R": "4", "D": "7", "L": "2", "U": "1"},
        "4": {"D": "8", "L": "3"},
        "5": {"R": "6"},
        "6": {"R": "7", "D": "A", "L": "5", "U": "2"},
        "7": {"R": "8", "D": "B", "L": "6", "U": "3"},
        "8": {"R": "9", "D": "C", "L": "7", "U": "4"},
        "9": {"L": "8"},
        "A": {"R": "B", "U": "6"},
        "B": {"R": "C", "D": "D", "L": "A", "U": "7"},
        "C": {"L": "B", "U": "8"},
        "D": {"U": "B"},
    }
    return _main(keypad)
