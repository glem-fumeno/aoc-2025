from abc import ABC, abstractmethod
from collections.abc import Iterable

type Position = tuple[int, ...]


def area_to(p1: Position, p2: Position) -> int:
    dx, dy = abs(p1[0] - p2[0]) + 1, abs(p1[1] - p2[1]) + 1
    return abs(dx * dy)


def edge_to(p1: Position, p2: Position) -> Edge:
    if p1[0] == p2[0]:
        return VerticalEdge(p1, p2)
    return HorizontalEdge(p1, p2)


def rectangle_to(p1: Position, p2: Position) -> list[Edge]:
    x1, y1 = p1
    x2, y2 = p2
    return [
        HorizontalEdge((x1, y1), (x2, y1)),
        HorizontalEdge((x1, y2), (x2, y2)),
        VerticalEdge((x1, y1), (x1, y2)),
        VerticalEdge((x2, y1), (x2, y2)),
    ]


class _Edge(ABC):
    __slots__ = "p1", "p2", "x", "y"
    p1: Position
    p2: Position

    def __init__(self, p1: Position, p2: Position) -> None:
        self.p1 = p1
        self.p2 = p2

    @property
    def vertices(self) -> tuple[Position, ...]:
        return self.p1, self.p2

    def other(self, p: Position) -> Position:
        return self.p1 if p == self.p2 else self.p2

    @abstractmethod
    def on_edge(self, p: Position) -> bool: ...

    @abstractmethod
    def iterate(self, xs: set[int], ys: set[int]) -> Iterable[Position]: ...


class VerticalEdge(_Edge):
    x: int

    def __init__(self, p1: Position, p2: Position) -> None:
        if p1[1] > p2[1]:
            p1, p2 = p2, p1
        super().__init__(p1, p2)
        assert p1[0] == p2[0]
        self.x = p1[0]

    def on_edge(self, p: Position) -> bool:
        return p[0] == self.x and self.p1[1] <= p[1] <= self.p2[1]

    def iterate(self, xs: set[int], ys: set[int]) -> Iterable[Position]:
        del xs
        return ((self.x, y) for y in ys if self.p1[1] <= y <= self.p2[1])


class HorizontalEdge(_Edge):
    y: int

    def __init__(self, p1: Position, p2: Position) -> None:
        if p1[0] > p2[0]:
            p1, p2 = p2, p1
        super().__init__(p1, p2)
        assert p1[1] == p2[1]
        self.y = p1[1]

    def on_edge(self, p: Position) -> bool:
        return p[1] == self.y and self.p1[0] <= p[0] <= self.p2[0]

    def iterate(self, xs: set[int], ys: set[int]) -> Iterable[Position]:
        del ys
        return ((x, self.y) for x in xs if self.p1[0] <= x <= self.p2[0])


type Edge = VerticalEdge | HorizontalEdge


def solve_09_part_1(file: str) -> int:
    positions = [tuple(map(int, line.split(","))) for line in file.splitlines()]
    return max(area_to(p1, p2) for p1 in positions for p2 in positions)


def is_inside(
    p: Position,
    vertices: set[Position],
    edges: list[Edge],
    vertical_edges: dict[int, VerticalEdge],
    cache: dict[Position, bool],
):
    if p in vertices:
        return True
    if p in cache:
        return cache[p]
    if any(edge.on_edge(p) for edge in edges):
        cache[p] = True
        return True
    positions = ((e.x, p[1]) for e in vertical_edges.values() if e.x < p[0])
    inside = False
    last_direction: bool | None = None
    for pos in positions:
        edge = vertical_edges[pos[0]]
        if not edge.on_edge(pos):
            continue
        if pos in edge.vertices and last_direction is None:
            last_direction = edge.other(pos)[1] > pos[1]
        elif pos in edge.vertices:
            if (edge.other(pos)[1] > pos[1]) != last_direction:
                inside = not inside
            last_direction = None
        else:
            inside = not inside
    cache[p] = inside
    return inside


def solve_09_part_2(file: str) -> int:
    positions = [tuple(map(int, line.split(","))) for line in file.splitlines()]
    vertices = set(positions)
    edges = [
        edge_to(positions[i], positions[(i + 1) % len(positions)])
        for i in range(len(positions))
    ]
    xs, ys = {p[0] for p in positions}, {p[1] for p in positions}
    vertical_edges = {e.x: e for e in edges if isinstance(e, VerticalEdge)}
    permutations = [
        (p1, p2, area_to(p1, p2))
        for p1 in positions
        for p2 in positions
        if hash(p1) < hash(p2)
    ]
    current_max = 0
    cache: dict[Position, bool] = {}
    for p1, p2, a in permutations:
        if a <= current_max:
            continue
        if all(
            is_inside(p, vertices, edges, vertical_edges, cache)
            for edge in rectangle_to(p1, p2)
            for p in edge.iterate(xs, ys)
        ):
            current_max = a
    return current_max
