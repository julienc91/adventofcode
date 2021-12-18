from hashlib import md5


def main_(suffix: str) -> int:
    secret = input().strip()
    i = 1
    while not md5(f"{secret}{i}".encode()).hexdigest().startswith(suffix):
        i += 1
    return i


def main1() -> int:
    return main_("00000")


def main2() -> int:
    return main_("000000")
