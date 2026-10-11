from collections import defaultdict


def solve_07_part_1(file: str) -> int:
    tachions = {i for i, t in enumerate(file.splitlines()[0]) if t == "S"}
    splits = 0
    for line in file.splitlines():
        next_tachions: set[int] = set()
        for tachion in tachions:
            match line[tachion]:
                case "^":
                    next_tachions.add(tachion - 1)
                    next_tachions.add(tachion + 1)
                    splits += 1
                case _:
                    next_tachions.add(tachion)
        tachions = next_tachions
    return splits


def solve_07_part_2(file: str) -> int:
    tachions: dict[int, int] = defaultdict(lambda: 0)
    tachions[next(i for i, t in enumerate(file.splitlines()[0]) if t == "S")] = 1
    for line in file.splitlines():
        next_tachions: dict[int, int] = defaultdict(lambda: 0)
        for tachion, splits in tachions.items():
            match line[tachion]:
                case "^":
                    next_tachions[tachion - 1] += splits
                    next_tachions[tachion + 1] += splits
                case _:
                    next_tachions[tachion] += splits
        tachions = next_tachions
    return sum(tachions.values())
