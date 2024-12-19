from collections import Counter, defaultdict

from utils.parsing import parse_input
from utils.regex import findone


def parse_lines() -> list[str]:
    return sorted(parse_input())


def aggregate_sleep_times() -> dict[int, Counter[int]]:
    guard_id = None
    asleep_since = None
    counters = defaultdict(Counter)
    for line in parse_lines():
        minutes = int(line[15:17])
        if "begins shift" in line:
            guard_id = int(findone(r"Guard #(\d+) begins shift", line))
            assert asleep_since is None
        elif "falls asleep" in line:
            assert asleep_since is None
            asleep_since = minutes
        elif "wakes up" in line:
            assert asleep_since is not None and asleep_since < minutes
            counters[guard_id].update(range(asleep_since, minutes))
            asleep_since = None
        else:
            raise ValueError(line)
    return counters


def main1() -> int:
    counters = aggregate_sleep_times()
    guard_id = max(counters, key=lambda id_: counters[id_].total())
    [(minutes, _)] = counters[guard_id].most_common(1)
    return guard_id * minutes


def main2() -> int:
    counters = aggregate_sleep_times()
    res = (0, 0, 0)

    for guard_id in counters:
        [value, count] = counters[guard_id].most_common(1)[0]
        res = max(res, (count, value, guard_id))

    _, minutes, guard_id = res
    return guard_id * minutes
