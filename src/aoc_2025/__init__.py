import sys
from pathlib import Path
from time import perf_counter
from typing import Any, Protocol

from aoc_2025.day_01 import Solution01
from aoc_2025.day_02 import Solution02
from aoc_2025.day_03 import Solution03
from aoc_2025.day_04 import Solution04
from aoc_2025.day_05 import Solution05
from aoc_2025.day_06 import Solution06
from aoc_2025.day_07 import Solution07
from aoc_2025.day_08 import Solution08
from aoc_2025.day_09 import Solution09
from aoc_2025.day_10 import Solution10


class Solution(Protocol):
    def __init__(self, file: str) -> None: ...
    def solve_part_1(self) -> Any: ...
    def solve_part_2(self) -> Any: ...


solution_by_name: dict[str, type[Solution]] = {
    "01": Solution01,
    "02": Solution02,
    "03": Solution03,
    "04": Solution04,
    "05": Solution05,
    "06": Solution06,
    "07": Solution07,
    "08": Solution08,
    "09": Solution09,
    "10": Solution10,
}


def solve(name: str):
    file = Path("./inputs").joinpath(name + ".txt").read_text().removesuffix("\n")
    init = perf_counter()
    solution = solution_by_name[name](file)
    start = perf_counter()
    solution_1 = solution.solve_part_1()
    mid = perf_counter()
    solution_2 = solution.solve_part_2()
    end = perf_counter()
    print(f"----- day {name} ({(end - init) * 1000:.1f}ms) -----")
    print(f"--- part 1 ({(mid - start) * 1000:.1f}ms) ---")
    print(solution_1)
    print(f"--- part 2 ({(end - mid) * 1000:.1f}ms) ---")
    print(solution_2)


def main() -> None:
    if len(sys.argv) <= 1:
        for name in solution_by_name:
            solve(name)
    else:
        solve(sys.argv[1])
