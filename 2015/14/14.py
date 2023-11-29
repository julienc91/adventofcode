from collections.abc import Iterator

from utils.parsing import parse_input


def parse_descriptions() -> Iterator[tuple[int, int, int]]:
    for line in parse_input():
        _, _, _, speed, _, _, duration, _, _, _, _, _, _, sleep, _ = line.split()
        yield int(speed), int(duration), int(sleep)


def evaluate1(speed: int, duration: int, sleep: int, stop_at: int) -> int:
    nb_full_cycles = stop_at // (duration + sleep)
    remaining = stop_at - (duration + sleep) * nb_full_cycles
    return nb_full_cycles * duration * speed + min(duration, remaining) * speed


class Reindeer:
    speed: int
    duration: int
    sleep: int

    score: int = 0
    position: int = 0

    def __init__(self, speed: int, duration: int, sleep: int) -> None:
        self.speed = speed
        self.duration = duration
        self.sleep = sleep

        self.score = 0
        self.position = 0

        self.is_resting = False
        self.seconds_before_next_phase = self.duration

    def pass_time(self, seconds: int) -> None:
        if seconds <= 0:
            return

        remaining = 0
        if self.seconds_before_next_phase < seconds:
            remaining = seconds - self.seconds_before_next_phase

        self.seconds_before_next_phase -= seconds
        if not self.is_resting:
            self.position += seconds * self.speed

        if self.seconds_before_next_phase == 0:
            self.is_resting = not self.is_resting
            self.seconds_before_next_phase = (
                self.sleep if self.is_resting else self.duration
            )

        if remaining:
            self.pass_time(remaining)


def main1() -> int:
    return max(
        evaluate1(*description, stop_at=2503) for description in parse_descriptions()
    )


def main2() -> int:
    reindeers = [
        Reindeer(speed=speed, duration=duration, sleep=sleep)
        for speed, duration, sleep in parse_descriptions()
    ]

    for _ in range(2503):
        best_position = 0
        for reindeer in reindeers:
            reindeer.pass_time(1)
            best_position = max(best_position, reindeer.position)
        for reindeer in reindeers:
            if reindeer.position == best_position:
                reindeer.score += 1

    reindeers.sort(key=lambda r: r.score)
    return reindeers[-1].score
