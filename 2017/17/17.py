from collections import deque


def main1() -> int:
    step = int(input())
    data = deque()
    for i in range(2018):
        data.rotate(-step)
        data.append(i)
    return data[(data.index(2017) + 1) % len(data)]


def main2() -> int:
    step = int(input())
    insertion_index = 0
    res = 0
    for i in range(1, 50_000_001):
        insertion_index = (insertion_index + step) % i + 1
        if insertion_index == 1:
            res = i
    return res
