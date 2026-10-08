from collections.abc import Generator, Iterable
from typing import Literal

type RollState = Literal[".", "@"]


class RollGrid:
    grid: list[list[bool]]
    width: int
    height: int

    def __init__(self, file: str) -> None:
        lines = file.splitlines()
        self.grid = [[c == "@" for c in line] for line in lines]
        self.height = len(lines)
        self.width = len(lines[0])

    def at_pos(self, r: int, c: int) -> bool:
        return (
            0 <= r <= self.height - 1 and 0 <= c <= self.width - 1 and self.grid[r][c]
        )

    def neighbours_at(self, r: int, c: int) -> int:
        return sum(
            [
                self.at_pos(r + 1, c + 1),
                self.at_pos(r + 1, c + 0),
                self.at_pos(r + 1, c - 1),
                self.at_pos(r + 0, c + 1),
                self.at_pos(r + 0, c - 1),
                self.at_pos(r - 1, c + 1),
                self.at_pos(r - 1, c + 0),
                self.at_pos(r - 1, c - 1),
            ]
        )

    def is_accessible(self, r: int, c: int) -> bool:
        return self.at_pos(r, c) and self.neighbours_at(r, c) < 4

    def remove_many(self, positions: Iterable[tuple[int, int]]):
        for r, c in positions:
            self.grid[r][c] = False

    def get_accessible(self) -> Generator[tuple[int, int]]:
        for r, row in enumerate(self.grid):
            for c, _ in enumerate(row):
                if self.is_accessible(r, c):
                    yield r, c


def solve_04_part_1(file: str) -> int:
    return len(list(RollGrid(file).get_accessible()))


def solve_04_part_2(file: str) -> int:
    grid = RollGrid(file)
    total = 0
    while len(to_remove := [(r, c) for r, c in grid.get_accessible()]) > 0:
        total += len(to_remove)
        grid.remove_many(to_remove)
    return total
