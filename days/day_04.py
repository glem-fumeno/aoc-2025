from typing import Self


class Tile:
    def __init__(self, ch: str) -> None:
        self.ch = ch
        self.neighbours: set[Self] = set()

    def remove(self):
        for neighbour in self.neighbours:
            neighbour.neighbours.remove(self)
        self.ch = "."

    @property
    def reachable(self) -> bool:
        if self.ch == ".":
            return False
        return len(self.neighbours) < 4


def get_tiles(grid: str):
    lines = grid.splitlines()
    h = len(lines)
    w = len(lines[0])
    tiles = [Tile(ch) for line in lines for ch in line]
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == ".":
                continue
            for i in range(max(y - 1, 0), min(y + 2, h)):
                for j in range(max(x - 1, 0), min(x + 2, w)):
                    if i * w + j == y * w + x:
                        continue
                    tiles[i * w + j].neighbours.add(tiles[y * w + x])
    return tiles


def solve_part_one(input_file: str):
    return sum(tile.reachable for tile in get_tiles(input_file))


def solve_part_two(input_file: str):
    tiles = get_tiles(input_file)
    total = 0
    while any(tile.reachable for tile in tiles):
        total += len([tile.remove() for tile in tiles if tile.reachable])
    return total
