import sys
from collections.abc import Callable
from pathlib import Path
from time import perf_counter
from typing import Any

from aoc_2025.day_01 import solve_01_part_1, solve_01_part_2
from aoc_2025.day_02 import solve_02_part_1, solve_02_part_2
from aoc_2025.day_03 import solve_03_part_1, solve_03_part_2
from aoc_2025.day_04 import solve_04_part_1, solve_04_part_2
from aoc_2025.day_05 import solve_05_part_1, solve_05_part_2

type Solution = Callable[[str], Any]
solutions_by_name: dict[str, tuple[Solution, Solution]] = {
    "01": (solve_01_part_1, solve_01_part_2),
    "02": (solve_02_part_1, solve_02_part_2),
    "03": (solve_03_part_1, solve_03_part_2),
    "04": (solve_04_part_1, solve_04_part_2),
    "05": (solve_05_part_1, solve_05_part_2),
}


def solve(name: str):
    solve_part_1, solve_part_2 = solutions_by_name[name]
    file = Path("./inputs").joinpath(name + ".txt").read_text().strip()
    start = perf_counter()
    solution_1 = solve_part_1(file)
    mid = perf_counter()
    solution_2 = solve_part_2(file)
    end = perf_counter()
    print(f"----- day {name} ({(end - start) * 1000:.1f}ms) -----")
    print(f"--- part 1 ({(mid - start) * 1000:.1f}ms) ---")
    print(solution_1)
    print(f"--- part 2 ({(end - mid) * 1000:.1f}ms) ---")
    print(solution_2)


def main() -> None:
    if len(sys.argv) <= 1:
        for name in solutions_by_name:
            solve(name)
    else:
        solve(sys.argv[1])
