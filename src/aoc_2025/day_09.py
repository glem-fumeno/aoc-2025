from collections.abc import Iterable


def between(le: int, v: int, ge: int) -> bool:
    return le <= v <= ge or ge <= v <= le


class Position:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def with_x(self, x: int) -> Position:
        return Position(x, self.y)

    def with_y(self, y: int) -> Position:
        return Position(self.x, y)

    def area_to(self, other: Position) -> int:
        dx, dy = abs(other.x - self.x) + 1, abs(other.y - self.y) + 1
        return abs(dx * dy)

    def rectangle_to(self, other: Position) -> list[Edge]:
        return [
            Edge(self, self.with_x(other.x)),
            Edge(self.with_x(other.x), other),
            Edge(other, self.with_y(other.y)),
            Edge(self.with_y(other.y), self),
        ]

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Position) and (self.x, self.y) == (value.x, value.y)

    def __repr__(self) -> str:
        return f"{self.x}x{self.y}y"


class Edge:
    p1: Position
    p2: Position
    x: int | None = None
    y: int | None = None

    def __init__(self, p1: Position, p2: Position) -> None:
        assert p1.x == p2.x or p1.y == p2.y, "Invalid edge"
        self.p1 = p1
        self.p2 = p2
        if self.p1.x == self.p2.x:
            self.x, self.y = p1.x, None
        if self.p1.y == self.p2.y:
            self.x, self.y = None, p1.y

    @property
    def vertices(self) -> tuple[Position, ...]:
        return self.p1, self.p2

    def other(self, p: Position) -> Position:
        return self.p1 if p == self.p2 else self.p2

    def on_edge(self, p: Position) -> bool:
        return self.on_vertical_edge(p) or self.on_horizontal_edge(p)

    def on_vertical_edge(self, p: Position) -> bool:
        return p.x == self.x and between(self.p1.y, p.y, self.p2.y)

    def on_horizontal_edge(self, p: Position) -> bool:
        return p.y == self.y and between(self.p1.x, p.x, self.p2.x)

    def iterate(self, xs: set[int], ys: set[int]) -> Iterable[Position]:
        if self.x is not None:
            for y in ys:
                if between(self.p1.y, y, self.p2.y):
                    yield Position(self.x, y)
        if self.y is not None:
            for x in xs:
                if between(self.p1.x, x, self.p2.x):
                    yield Position(x, self.y)


def solve_09_part_1(file: str) -> int:
    positions = [Position(*map(int, line.split(","))) for line in file.splitlines()]
    return max(p1.area_to(p2) for p1 in positions for p2 in positions)


def is_inside(
    p: Position,
    vertices: list[Position],
    edges: list[Edge],
    cache: dict[Position, bool],
):
    if p in cache:
        return cache[p]
    if p in vertices:
        cache[p] = True
        return True
    if any(edge.on_edge(p) for edge in edges):
        cache[p] = True
        return True
    positions = [Position(e.x, p.y) for e in edges if e.x is not None and e.x < p.x]
    inside = False
    last_direction: bool | None = None
    for pos in positions:
        for edge in edges:
            if not edge.on_vertical_edge(pos):
                continue
            if pos in edge.vertices and last_direction is None:
                last_direction = edge.other(pos).y > pos.y
            elif pos in edge.vertices:
                if (edge.other(pos).y > pos.y) != last_direction:
                    inside = not inside
                last_direction = None
            else:
                inside = not inside
            break
    cache[p] = inside
    return inside


def solve_09_part_2(file: str) -> int:
    positions = [Position(*map(int, line.split(","))) for line in file.splitlines()]
    edges = [
        Edge(positions[i], positions[(i + 1) % len(positions)])
        for i in range(len(positions))
    ]
    cache: dict[Position, bool] = {}
    xs = {p.x + i for p in positions for i in range(-1, 2)}
    ys = {p.y + i for p in positions for i in range(-1, 2)}
    permutations = [
        (p1, p2, print(f"{i * len(positions) + j} / {len(positions) * len(positions)}"))
        for i, p1 in enumerate(positions)
        for j, p2 in enumerate(positions)
        if hash(p1) < hash(p2)
        and all(
            is_inside(p, positions, edges, cache)
            for edge in p1.rectangle_to(p2)
            for p in edge.iterate(xs, ys)
        )
    ]
    return max(p1.area_to(p2) for p1, p2, _ in permutations)
