import sys
from importlib import import_module
from pathlib import Path

puzzles = [
    "01",
    "02",
]


def solve(name: str):
    module = import_module(f"days.day_{name}")
    file = Path("./inputs").joinpath(f"day_{name}.txt").read_text().strip()
    return f"{module.solve_part_one(file)} x {module.solve_part_two(file)}"


def main():
    args = sys.argv
    if len(args) == 2:
        if args[-1] == "-h":
            print(*puzzles)
            return
        print(solve(args[1]))
    else:
        for name in puzzles:
            result = solve(name)
            print(
                " " * (max(map(len, puzzles)) - len(name)), f"{name}: {result}"
            )


if __name__ == "__main__":
    main()
