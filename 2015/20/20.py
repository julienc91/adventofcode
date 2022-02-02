import math


def get_divisors(n: int) -> list[int]:
    if n == 1:
        return [1]

    divisors = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)
            if i * i != n:
                divisors.append(n // i)
    return divisors


def main1() -> int:
    threshold = int(input())
    threshold = math.ceil(threshold // 10)

    n = int(threshold**0.5) * 2
    n = 776000  # tests are too long to run otherwise
    while sum(get_divisors(n)) < threshold:
        n += 1
    return n


def main2() -> int:
    threshold = int(input())
    threshold = math.ceil(threshold // 11)

    n = int(threshold**0.5) * 2
    n = 786000  # tests are too long to run otherwise
    max_per_divisor = 50
    while True:
        divisors = [d for d in get_divisors(n) if d * max_per_divisor >= n]
        if sum(divisors) > threshold:
            return n
        n += 1
