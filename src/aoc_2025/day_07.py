from collections import defaultdict


class Solution07:
    def __init__(self, file: str) -> None:
        self.tachion = next(i for i, t in enumerate(file.splitlines()[0]) if t == "S")
        self.lines = file.splitlines()

    def solve_part_1(self) -> int:
        tachions = {self.tachion}
        splits = 0
        for line in self.lines:
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

    def solve_part_2(self) -> int:
        tachions: dict[int, int] = defaultdict(lambda: 0)
        tachions[self.tachion] = 1
        for line in self.lines:
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
