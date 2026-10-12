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

    def area_to(self, other: Position) -> int:
        dx, dy = abs(other.x - self.x) + 1, abs(other.y - self.y) + 1
        return abs(dx * dy)

    def __eq__(self, value: Position, /) -> bool:  # pyright: ignore[reportIncompatibleMethodOverride]
        return (self.x, self.y) == (value.x, value.y)

    def __repr__(self) -> str:
        return f"{self.x}x{self.y}y)"


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

    def on_edge(self, p: Position) -> bool:
        return self.on_vertical_edge(p) or self.on_horizontal_edge(p)

    def on_vertical_edge(self, p: Position) -> bool:
        return p.x == self.x and between(self.p1.y, p.y, self.p2.y)

    def on_horizontal_edge(self, p: Position) -> bool:
        return p.y == self.y and between(self.p1.x, p.x, self.p2.x)


def solve_09_part_1(file: str) -> int:
    positions = [Position(*map(int, line.split(","))) for line in file.splitlines()]
    return max(p1.area_to(p2) for p1 in positions for p2 in positions)


def solve_09_part_2(file: str) -> int:
    positions = [Position(*map(int, line.split(","))) for line in file.splitlines()]
    edges = [
        Edge(positions[i], positions[(i + 1) % len(positions)])
        for i in range(len(positions))
    ]
    max_x = max(p.x for p in positions)
    max_y = max(p.y for p in positions)
    for i in range(max_y + 2):
        for j in range(max_x + 2):
            p = Position(j, i)
            if p in positions:
                print("x", end="")
                continue
            for edge in edges:
                if edge.on_vertical_edge(p):
                    print("|", end="")
                    break
                if edge.on_horizontal_edge(p):
                    print("-", end="")
                    break
            else:
                print(".", end="")
        print()
    return 0
