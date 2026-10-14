type Position = tuple[int, ...]


def from_csv(line: str) -> Position:
    return tuple(map(int, line.split(",")))


def distance_to_sq(p1: Position, p2: Position) -> int:
    dx, dy, dz = p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]
    return dx * dx + dy * dy + dz * dz


class Solution08:
    def __init__(self, file: str) -> None:
        self.file = file
        self.positions = {from_csv(line) for line in self.file.splitlines()}
        self.permutations = sorted(
            [
                (p1, p2)
                for p1 in self.positions
                for p2 in self.positions
                if hash(p1) < hash(p2)
            ],
            key=lambda v: distance_to_sq(v[0], v[1]),
        )

    def solve_part_1(self) -> int:
        circuits = [{p} for p in self.positions]
        for p1, p2 in self.permutations[:1000]:
            s1 = next(s for s in circuits if p1 in s)
            s2 = next(s for s in circuits if p2 in s)
            c: list[set[Position]] = [s for s in circuits if {p1, p2}.isdisjoint(s)]
            c.append(s1.union(s2))
            circuits = c
        l1, l2, l3, *_ = sorted(map(len, circuits), reverse=True)
        return l1 * l2 * l3

    def solve_part_2(self) -> int:
        circuits = [{p} for p in self.positions]
        p1 = (0, 0, 0)
        p2 = (0, 0, 0)
        for p1, p2 in self.permutations:
            s1 = next(s for s in circuits if p1 in s)
            s2 = next(s for s in circuits if p2 in s)
            circuits: list[set[Position]] = [
                s for s in circuits if {p1, p2}.isdisjoint(s)
            ]
            circuits.append(s1.union(s2))
            if len(circuits) <= 1:
                break
        return p1[0] * p2[0]
