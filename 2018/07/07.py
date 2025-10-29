from utils.parsing import parse_input


def main1() -> str:
    steps: dict[str, set[str]] = {}
    for line in parse_input():
        _, a, _, _, _, _, _, b, _, _ = line.split()
        steps.setdefault(a, set())
        steps.setdefault(b, set())
        steps[b].add(a)

    res = ""
    while steps:
        next_step = min(step for step in steps if len(steps[step]) == 0)
        for step in steps:
            steps[step].discard(next_step)
        steps.pop(next_step)
        res += next_step
    return res


def main2() -> int:
    steps: dict[str, tuple[int, set[str]]] = {}
    for line in parse_input():
        _, a, _, _, _, _, _, b, _, _ = line.split()
        steps.setdefault(a, (60 + ord(a) - ord("A") + 1, set()))
        steps.setdefault(b, (60 + ord(b) - ord("A") + 1, set()))
        steps[b][1].add(a)

    total = -1
    workers: list[str | None] = [None] * 5
    while steps:
        if any(workers):
            next_time_jump = min(steps[worker][0] for worker in workers if worker)
        else:
            next_time_jump = 1

        for i, current_step in enumerate(workers):
            if current_step is not None:
                time_left, deps = steps[current_step]
                time_left -= next_time_jump
                if time_left == 0:
                    for step in steps:
                        steps[step][1].discard(current_step)
                    steps.pop(current_step)
                    workers[i] = None
                else:
                    steps[current_step] = (time_left, deps)

        while not all(workers):
            try:
                next_step = min(
                    step
                    for step in steps
                    if len(steps[step][1]) == 0 and step not in workers
                )
            except ValueError:
                break
            workers.remove(None)
            workers.append(next_step)

        total += next_time_jump

    return total
