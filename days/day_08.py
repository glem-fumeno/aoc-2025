Node = tuple[int, int, int]

distances: dict[tuple[Node, Node], int] = {}


def distance_sq(n1: Node, n2: Node) -> int:
    x1, y1, z1 = n1
    x2, y2, z2 = n2
    x, y, z = (x1 - x2), (y1 - y2), (z1 - z2)
    return x * x + y * y + z * z


def get_distances(nodes: list[Node]):
    for src in nodes:
        for dst in nodes:
            if src == dst or (dst, src) in distances:
                continue
            distances[src, dst] = distance_sq(src, dst)


def solve_part_one(input_file: str):
    nodes: list[Node] = []
    groups: list[set[Node]] = []
    for line in input_file.splitlines():
        x, y, z = map(int, line.split(","))
        nodes.append((x, y, z))
        groups.append({(x, y, z)})
    if len(distances) < 1:
        get_distances(nodes)
    for (src, dst), _ in sorted(distances.items(), key=lambda x: x[1])[:1000]:
        future_group = set()
        to_remove = []
        for group in groups:
            if src in group or dst in group:
                to_remove.append(group)
                future_group = future_group.union(group)
        for group in to_remove:
            groups.remove(group)
        groups.append(future_group)
    final_groups = sorted((len(group) for group in groups), reverse=True)
    return final_groups[0] * final_groups[1] * final_groups[2]


def solve_part_two(input_file: str):
    nodes: list[Node] = []
    groups: list[set[Node]] = []
    for line in input_file.splitlines():
        x, y, z = map(int, line.split(","))
        nodes.append((x, y, z))
        groups.append({(x, y, z)})
    if len(distances) < 1:
        get_distances(nodes)
    for (src, dst), _ in sorted(distances.items(), key=lambda x: x[1]):
        future_group = set()
        to_remove = []
        for group in groups:
            if src in group or dst in group:
                to_remove.append(group)
                future_group = future_group.union(group)
        for group in to_remove:
            groups.remove(group)
        if len(groups) < 1:
            break
        groups.append(future_group)
    return src[0] * dst[0]
