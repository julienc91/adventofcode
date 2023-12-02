import importlib
from collections.abc import Callable
from typing import Any

import pytest

from cli.utils.puzzle import run_puzzle_func

EXPECTED_RESULTS: dict[int, list[tuple[int, tuple[int | str, int | str]]]] = {
    2023: [
        (1, (54951, 55218)),
        (2, (2593, 54699)),
    ],
    2022: [
        (1, (67633, 199628)),
        (2, (10624, 14060)),
        (3, (7817, 2444)),
        (4, (644, 926)),
        (5, ("FRDSQRRCD", "HRFTQVWNN")),
        (6, (1655, 2665)),
        (7, (1749646, 1498966)),
        (8, (1823, 211680)),
        (9, (6357, 2627)),
        (10, (15020, "EFUGLPAP")),
        (11, (50172, 11614682178)),
        (12, (528, 522)),
        (13, (6568, 19493)),
        (14, (961, 26375)),
        (15, (4873353, 11600823139120)),
        (16, (1915, 2772)),
        (17, (3168, 1554117647070)),
        (18, (4364, 2508)),
        (19, (2160, 13340)),
        (20, (5962, 9862431387256)),
        (21, (66174565793494, 3327575724809)),
        (22, (55244, 123149)),
        (23, (3917, 988)),
        (24, (326, 976)),
        (25, ("2=0--0---11--01=-100", -1)),
    ],
    2021: [
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
        (12, (4775, 152480)),
        (13, (785, -1)),
        (14, (3143, 4110215602456)),
        (15, (581, 2916)),
        (16, (938, 1495959086337)),
        (17, (7381, 3019)),
        (18, (3691, 4756)),
        (19, (367, 11925)),
        (20, (5498, 16014)),
        (21, (506466, 632979211251440)),
        (22, (561032, 1322825263376414)),
    ],
    2017: [
        (1, (1175, 1166)),
        (2, (21845, 191)),
        (3, (438, 266330)),
        (4, (451, 223)),
        (5, (373160, 26395586)),
        (6, (7864, 1695)),
        (7, ("rqwgj", 333)),
        (8, (6343, 7184)),
        (9, (17390, 7825)),
        (10, (4480, "c500ffe015c83b60fad2e4b7d59dabc4")),
        (11, (747, 1544)),
        (12, (288, 211)),
        (13, (1528, 3896406)),
        (14, (8230, 1103)),
        (15, (573, 294)),
        (16, ("jcobhadfnmpkglie", "pclhmengojfdkaib")),
        (17, (1311, 39170601)),
        (18, (3423, 7493)),
    ],
    2016: [
        (1, (230, 154)),
        (2, ("61529", "C2C28")),
        (3, (869, 1544)),
        (4, (173787, 548)),
        (5, ("c6697b55", "8c35d1ab")),
        (6, ("ikerpcty", "uwpfaqrq")),
        (7, (115, 231)),
        (8, (106, "CFLELOYFCS")),
        (9, (112830, 10931789799)),
        (10, (93, 47101)),
        (11, (33, 57)),
        (12, (318117, 9227771)),
        (13, (96, 141)),
        (14, (15168, 20864)),
        (15, (376777, 3903937)),
        (16, (10011010010010010, 10101011110100011)),
        (17, ("RDURRDDLRD", 526)),
        (18, (1961, 20000795)),
        (19, (1834471, 1420064)),
        (20, (14975795, 101)),
        (21, ("fdhbcgea", "egfbcadh")),
        (22, (955, 246)),
        (23, (12516, 479009076)),
        (24, (412, 664)),
        (25, (192, -1)),
    ],
    2015: [
        (1, (74, 1795)),
        (2, (1606483, 3842356)),
        (3, (2081, 2341)),
        (4, (254575, 1038736)),
        (5, (236, 51)),
        (6, (569999, 17836115)),
        (7, (3176, 14710)),
        (8, (1350, 2085)),
        (9, (141, 736)),
        (10, (492982, 6989950)),
        (11, ("hepxxyzz", "heqaabcc")),
        (12, (119433, 68466)),
        (13, (618, 601)),
        (14, (2696, 1084)),
        (15, (13882464, 11171160)),
        (16, (213, 323)),
        (17, (1638, 17)),
        (18, (1061, 1006)),
        (19, (576, 207)),
        (20, (776160, 786240)),
        (21, (111, 188)),
        (22, (1824, 1937)),
        (23, (170, 247)),
        (24, (10439961859, 72050269)),
        (25, (2650453, -1)),
    ],
}

TEST_PARAMETERS = [
    pytest.param(year, puzzle_id, result, id=f"{year}-{puzzle_id:02d}")
    for year in EXPECTED_RESULTS
    for puzzle_id, result in EXPECTED_RESULTS[year]
]


def run_test(year: int, puzzle_name: str, func_name: str) -> int | str:
    file_name = f"{year}.{puzzle_name}.{puzzle_name}"
    module = importlib.import_module(file_name)
    func: Callable[[], int | str] = getattr(module, func_name)
    return func()


@pytest.mark.parametrize("year, puzzle_name, expected_result", TEST_PARAMETERS)
def test_puzzle(
    year: int,
    puzzle_name: int,
    expected_result: tuple[int | str, int | str],
) -> None:
    result = run_puzzle_func(year, puzzle_name, "main1")
    assert result == expected_result[0]

    result = run_puzzle_func(year, puzzle_name, "main2")
    assert result == expected_result[1]


@pytest.mark.parametrize("year, puzzle_name, expected_result", TEST_PARAMETERS)
@pytest.mark.parametrize("part", [1, 2])
@pytest.mark.benchmark
def test_benchmark(
    benchmark: Any, year: int, puzzle_name: str, expected_result: str, part: int
) -> None:
    benchmark(run_puzzle_func, year, puzzle_name, f"main{part}")
