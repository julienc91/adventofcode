a_mul, b_mul = 16807, 48271
divider = 2**31 - 1
modulo = 2**16 - 1


def main1() -> int:
    a = int(input().strip().split()[-1])
    b = int(input().strip().split()[-1])

    count = 0
    total = 40_000_000
    for _ in range(total):
        a = (a * a_mul) % divider
        b = (b * b_mul) % divider
        if (a & modulo) == (b & modulo):
            count += 1
    return count


def main2() -> int:
    a = int(input().strip().split()[-1])
    b = int(input().strip().split()[-1])
    a_modulo, b_modulo = 4, 8

    count = 0
    total = 5_000_000
    for _ in range(total):
        while (a := (a * a_mul) % divider) % a_modulo != 0:
            pass
        while (b := (b * b_mul) % divider) % b_modulo != 0:
            pass
        if (a & modulo) == (b & modulo):
            count += 1
    return count


if __name__ == "__main__":
    print(main2())
