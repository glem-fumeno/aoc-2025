from collections.abc import Iterable
from functools import lru_cache

type Position = tuple[int, ...]
POS_X, POS_Y = 0, 1

type Edge = tuple[bool, int, int, int]
IS_VERTICAL, COMMON, SMALLER, LARGER = 0, 1, 2, 3


def area_to(p1: Position, p2: Position) -> int:
    dx, dy = abs(p1[POS_X] - p2[POS_X]) + 1, abs(p1[POS_Y] - p2[POS_Y]) + 1
    return abs(dx * dy)


def rectangle_to(p1: Position, p2: Position) -> list[Edge]:
    x1, y1 = p1
    x2, y2 = p2
    return [
        edge_to((x1, y1), (x2, y1)),
        edge_to((x1, y2), (x2, y2)),
        edge_to((x1, y1), (x1, y2)),
        edge_to((x2, y1), (x2, y2)),
    ]


def edge_to(p1: Position, p2: Position) -> Edge:
    if p1[POS_X] == p2[POS_X] and p1[POS_Y] > p2[POS_Y]:
        return True, p1[POS_X], p2[POS_Y], p1[POS_Y]
    elif p1[POS_X] == p2[POS_X]:
        return True, p1[POS_X], p1[POS_Y], p2[POS_Y]
    elif p1[POS_X] > p2[POS_X]:
        return False, p1[POS_Y], p2[POS_X], p1[POS_X]
    else:
        return False, p1[POS_Y], p1[POS_X], p2[POS_X]


class Solution09:
    def __init__(self, file: str) -> None:
        self.positions = [
            tuple(map(int, line.split(","))) for line in file.splitlines()
        ]
        self.vertices = set(self.positions)
        self.permutations = [
            (p1, p2, area_to(p1, p2))
            for p1 in self.positions
            for p2 in self.positions
            if hash(p1) < hash(p2)
        ]
        self.edges = [
            edge_to(self.positions[i], self.positions[(i + 1) % len(self.positions)])
            for i in range(len(self.positions))
        ]
        self.vertical_edges = {e[COMMON]: e for e in self.edges if e[IS_VERTICAL]}
        self.horizontal_edges = {e[COMMON]: e for e in self.edges if not e[IS_VERTICAL]}
        self.xs = {p[POS_X] for p in self.positions}
        self.ys = {p[POS_Y] for p in self.positions}

    def solve_part_1(self) -> int:
        return max(a for _, _, a in self.permutations)

    def solve_part_2(self) -> int:
        current_max = 0
        for p1, p2, a in self.permutations:
            if a <= current_max:
                continue
            if all(
                self.is_inside(p)
                for edge in rectangle_to(p1, p2)
                for p in self.iterate_edge(edge)
            ):
                current_max = a
        return current_max

    def iterate_edge(self, edge: Edge) -> Iterable[Position]:
        if edge[IS_VERTICAL]:
            return (
                (edge[COMMON], y) for y in self.ys if edge[SMALLER] <= y <= edge[LARGER]
            )
        return (
            (x, edge[COMMON]) for x in self.xs if edge[SMALLER] <= x <= edge[LARGER]
        )

    @lru_cache(None)
    def is_inside(self, p: Position):
        if p in self.vertices:
            return True
        edge = self.horizontal_edges[p[POS_Y]]
        if edge[SMALLER] <= p[POS_X] <= edge[LARGER]:
            return True
        edge = self.vertical_edges[p[POS_X]]
        if edge[SMALLER] <= p[POS_Y] <= edge[LARGER]:
            return True
        positions = (
            (e[COMMON], p[POS_Y])
            for e in self.vertical_edges.values()
            if e[COMMON] < p[POS_X] and e[SMALLER] <= p[POS_Y] <= e[LARGER]
        )
        inside = False
        last_dir: bool | None = None
        for pos in positions:
            edge = self.vertical_edges[pos[POS_X]]
            if last_dir is None and pos[POS_Y] == edge[SMALLER]:
                last_dir = edge[LARGER] > pos[POS_Y]
            elif last_dir is None and pos[POS_Y] == edge[LARGER]:
                last_dir = edge[SMALLER] > pos[POS_Y]
            elif pos[POS_Y] == edge[SMALLER]:
                if edge[LARGER] > pos[POS_Y] != last_dir:
                    inside = not inside
                last_dir = None
            elif pos[POS_Y] == edge[LARGER]:
                if (edge[SMALLER] > pos[POS_Y]) != last_dir:
                    inside = not inside
                last_dir = None
            else:
                inside = not inside
        return inside
