import re


def react(polymer: str) -> int:
    left, right = 0, len(polymer) - 1
    while True:
        idx = left
        at_least_one_reaction = False
        new_right = left
        while idx < right:
            a, b = polymer[idx], polymer[idx + 1]
            if a != b and a.lower() == b.lower():
                polymer = polymer[:idx] + polymer[idx + 2 :]
                if not at_least_one_reaction:
                    left = max(idx - 1, 0)

                right -= 2
                new_right = min(idx, len(polymer) - 1)
                at_least_one_reaction = True
            else:
                idx += 1

        if not at_least_one_reaction:
            break

        right = new_right

    return len(polymer)


def main1() -> int:
    polymer = input()
    return react(polymer)


def main2() -> int:
    polymer = input()
    letters = set(polymer.lower())
    return min(
        react(re.sub(letter, "", polymer, flags=re.IGNORECASE)) for letter in letters
    )
