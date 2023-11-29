from utils.parsing import parse_input


def parse_descriptions() -> list[dict[str, int]]:
    res: list[dict[str, int]] = []
    for line in parse_input():
        line = line.replace(":", "").replace(",", "")
        _, _, t1, c1, t2, c2, t3, c3 = line.split(" ")
        res.append(
            {
                t1: int(c1),
                t2: int(c2),
                t3: int(c3),
            }
        )
    return res


analysis = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def main1() -> int:
    descriptions = parse_descriptions()
    for i, description in enumerate(descriptions, start=1):
        for t, c in analysis.items():
            if t not in description:
                continue
            elif description[t] != c:
                break
        else:
            return i
    return -1


def main2() -> int:
    descriptions = parse_descriptions()
    for i, description in enumerate(descriptions, start=1):
        for t, c in analysis.items():
            if t not in description:
                continue
            elif t in ["cats", "trees"]:
                if description[t] <= c:
                    break
            elif t in ["pomeranians", "goldfish"]:
                if description[t] >= c:
                    break
            elif description[t] != c:
                break
        else:
            return i
    return -1
