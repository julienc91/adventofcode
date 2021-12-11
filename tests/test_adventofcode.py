import importlib
import io
import os

import pytest

EXPECTED_RESULTS = [
    (1, (1557, 1608)),
    (2, (1690020, 1408487760)),
    (3, (3687446, 4406844)),
    (4, (41503, 3178)),
    (5, (6283, 18864)),
    (6, (345793, 1572643095893)),
    (7, (349812, 99763899)),
    (8, (349, 1070957)),
    (9, (516, 1023660)),
    (10, (311949, 3042730309)),
    (11, (1721, 298)),
]


def run_test(puzzle_name: str, func_name: str) -> int:
    file_name = f"{puzzle_name}.{puzzle_name}"
    module = importlib.import_module(file_name)
    return getattr(module, func_name)()


@pytest.mark.parametrize("puzzle_id, expected_result", EXPECTED_RESULTS)
def test_puzzle(monkeypatch, puzzle_id: int, expected_result: tuple[int, int]) -> None:
    puzzle_name = f"{puzzle_id:02d}"
    with open(os.path.join(puzzle_name, "input")) as f:
        data = f.read()

    monkeypatch.setattr("sys.stdin", io.StringIO(data))
    result = run_test(puzzle_name, "main1")
    assert result == expected_result[0]

    monkeypatch.setattr("sys.stdin", io.StringIO(data))
    result = run_test(puzzle_name, "main2")
    assert result == expected_result[1]
