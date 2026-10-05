from collections.abc import Callable
from pathlib import Path
from typing import Any
from time import perf_counter

from aoc_2025.day_01 import solve_01_part_1, solve_01_part_2

type Solution = Callable[[str], Any]
solutions_by_name: dict[str, tuple[Solution, Solution]] = {
    "01": (solve_01_part_1, solve_01_part_2)
}


def main() -> None:
    for name, (solve_part_1, solve_part_2) in solutions_by_name.items():
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
