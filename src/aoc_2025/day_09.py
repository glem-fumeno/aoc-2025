from collections.abc import Iterable

type Position = tuple[int, ...]
POS_X, POS_Y = 0, 1


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


# is_vertical, common, n1, n2
type Edge = tuple[bool, int, int, int]
IS_VERTICAL, COMMON, SMALLER, LARGER = 0, 1, 2, 3


def edge_to(p1: Position, p2: Position) -> Edge:
    if p1[POS_X] == p2[POS_X] and p1[POS_Y] > p2[POS_Y]:
        return True, p1[POS_X], p2[POS_Y], p1[POS_Y]
    elif p1[POS_X] == p2[POS_X]:
        return True, p1[POS_X], p1[POS_Y], p2[POS_Y]
    elif p1[POS_X] > p2[POS_X]:
        return False, p1[POS_Y], p2[POS_X], p1[POS_X]
    else:
        return False, p1[POS_Y], p1[POS_X], p2[POS_X]


def iterate_edge(edge: Edge, xs: set[int], ys: set[int]) -> Iterable[Position]:
    if edge[IS_VERTICAL]:
        return ((edge[COMMON], y) for y in ys if edge[SMALLER] <= y <= edge[LARGER])
    return ((x, edge[COMMON]) for x in xs if edge[SMALLER] <= x <= edge[LARGER])


def solve_09_part_1(file: str) -> int:
    positions = [tuple(map(int, line.split(","))) for line in file.splitlines()]
    return max(area_to(p1, p2) for p1 in positions for p2 in positions)


def is_inside(
    p: Position,
    vertices: set[Position],
    horizontal_edges: dict[int, Edge],
    vertical_edges: dict[int, Edge],
    cache: dict[Position, bool],
):
    if p in cache:
        return cache[p]
    if p in vertices:
        return True
    edge = horizontal_edges[p[POS_Y]]
    if edge[SMALLER] <= p[POS_X] <= edge[LARGER]:
        return True
    edge = vertical_edges[p[POS_X]]
    if edge[SMALLER] <= p[POS_Y] <= edge[LARGER]:
        return True
    positions = (
        (e[COMMON], p[POS_Y])
        for e in vertical_edges.values()
        if e[COMMON] < p[POS_X] and e[SMALLER] <= p[POS_Y] <= e[LARGER]
    )
    inside = False
    last_dir: bool | None = None
    for pos in positions:
        edge = vertical_edges[pos[POS_X]]
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
    cache[p] = inside
    return inside


def solve_09_part_2(file: str) -> int:
    positions = [tuple(map(int, line.split(","))) for line in file.splitlines()]
    vertices = set(positions)
    edges = [
        edge_to(positions[i], positions[(i + 1) % len(positions)])
        for i in range(len(positions))
    ]
    xs, ys = {p[POS_X] for p in positions}, {p[POS_Y] for p in positions}
    vertical_edges = {e[COMMON]: e for e in edges if e[IS_VERTICAL]}
    horizontal_edges = {e[COMMON]: e for e in edges if not e[IS_VERTICAL]}
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
            is_inside(p, vertices, horizontal_edges, vertical_edges, cache)
            for edge in rectangle_to(p1, p2)
            for p in iterate_edge(edge, xs, ys)
        ):
            current_max = a
    return current_max
