from collections import Counter

from utils.parsing import parse_input


def main1() -> int:
    result = 0
    for line in parse_input():
        line = line.split("|")[1]
        digits = line.split()
        result += sum(1 for digit in digits if len(digit) in (2, 3, 4, 7))
    return result


def main2() -> int:
    result = 0
    for line in parse_input():
        left_part, right_part = line.split("|")
        all_digits = ["".join(sorted(digit)) for digit in left_part.strip().split(" ")]
        output_digits = [
            "".join(sorted(digit)) for digit in right_part.strip().split(" ")
        ]

        number_mapping = {
            1: next(d for d in all_digits if len(d) == 2),
            4: next(d for d in all_digits if len(d) == 4),
            7: next(d for d in all_digits if len(d) == 3),
            8: next(d for d in all_digits if len(d) == 7),
        }

        signals_counter = Counter("".join(all_digits))
        signals_mapping = {
            "b": next(c for c, count in signals_counter.items() if count == 6),
            "e": next(c for c, count in signals_counter.items() if count == 4),
            "f": next(c for c, count in signals_counter.items() if count == 9),
        }

        number_mapping[2] = next(
            d for d in all_digits if len(d) == 5 and signals_mapping["e"] in d
        )
        number_mapping[5] = next(
            d for d in all_digits if len(d) == 5 and signals_mapping["b"] in d
        )
        number_mapping[3] = next(
            d
            for d in all_digits
            if len(d) == 5 and d != number_mapping[2] and d != number_mapping[5]
        )
        number_mapping[9] = next(
            d for d in all_digits if len(d) == 6 and signals_mapping["e"] not in d
        )
        number_mapping[6] = next(
            d
            for d in all_digits
            if len(d) == 6
            and d != number_mapping[9]
            and all(c in d for c in number_mapping[5])
        )
        number_mapping[0] = next(
            d
            for d in all_digits
            if len(d) == 6 and d != number_mapping[9] and d != number_mapping[6]
        )

        reverse_number_mapping = {v: k for k, v in number_mapping.items()}

        result += int(
            "".join(str(reverse_number_mapping[digit]) for digit in output_digits)
        )
    return result
