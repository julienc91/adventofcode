from collections import defaultdict


def get_hash(string: str) -> int:
    res = 0
    for c in string:
        res = ((res + ord(c)) * 17) % 256
    return res


def main1() -> int:
    total = 0
    for operation in input().split(","):
        total += get_hash(operation)
    return total


def main2() -> int:
    boxes = defaultdict(list)
    focals_mapping = {}
    for operation in input().split(","):
        if "=" in operation:
            label, focal_length = operation.split("=")
            box_number = get_hash(label)
            if label not in boxes[box_number]:
                boxes[box_number].append(label)
            focals_mapping[(box_number, label)] = int(focal_length)
        else:
            label = operation[:-1]
            box_number = get_hash(label)
            try:
                boxes[box_number].remove(label)
                focals_mapping.pop((box_number, label))
            except ValueError:
                pass

    focusing_power = 0
    for box_number in range(256):
        box_score = 0
        for lens_number, label in enumerate(boxes[box_number]):
            box_score += (
                (box_number + 1)
                * (lens_number + 1)
                * focals_mapping[(box_number, label)]
            )
        focusing_power += box_score
    return focusing_power
