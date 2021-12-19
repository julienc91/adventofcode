def is_valid(password: str) -> bool:
    a, b = password[0], password[1]
    pairs = set()
    if a == b:
        pairs.add(a + b)

    found_triplet = False

    for i, c in enumerate(password[2:]):
        if c == b and (b + c) not in pairs:
            pairs.add(b + c)
        if ord(c) == ord(b) + 1 and ord(b) == ord(a) + 1:
            found_triplet = True
        a, b = b, c

    return found_triplet and len(pairs) >= 2


def next_char(c: str) -> str:
    if c == "z":
        return "a"
    return chr(ord(c) + 1)


def increment(password: str) -> str:
    def _increment(p: str) -> str:
        array = list(p)[::-1]
        updated_array = array[:]

        for i, c in enumerate(array):
            new_c = next_char(c)
            if new_c == "a":
                updated_array[i] = new_c
                continue

            if new_c in "ilo":
                new_c = next_char(new_c)
                for j in range(i):
                    updated_array[j] = "a"

            updated_array[i] = new_c
            break

        return "".join(updated_array[::-1])

    while True:
        password = _increment(password)
        if is_valid(password):
            return password


def main1() -> str:
    current_password = input().strip()
    new_password = increment(current_password)
    return new_password


def main2() -> str:
    current_password = input().strip()
    new_password = increment(current_password)
    return increment(new_password)
