from dataclasses import dataclass
from typing import Self


@dataclass
class Position:
    x: int
    y: int
    z: int

    @classmethod
    def from_csv(cls, line: str) -> Self:
        return cls(*map(int, line.split(",")))

    def distance_to_sq(self, other: Self) -> int:
        dx, dy, dz = other.x - self.x, other.y - self.y, other.z - self.z
        return dx * dx + dy * dy + dz * dz

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __repr__(self) -> str:
        return f"Position({self.x}, {self.y}, {self.z})"


def solve_08_part_1(file: str) -> int:
    positions = {Position.from_csv(line) for line in file.splitlines()}
    permutations = sorted(
        [(p1, p2) for p1 in positions for p2 in positions if hash(p1) < hash(p2)],
        key=lambda v: v[0].distance_to_sq(v[1]),
    )
    circuits = [{p} for p in positions]
    for p1, p2 in permutations[:1000]:
        s1 = next(s for s in circuits if p1 in s)
        s2 = next(s for s in circuits if p2 in s)
        c: list[set[Position]] = [s for s in circuits if {p1, p2}.isdisjoint(s)]
        c.append(s1.union(s2))
        circuits = c
    l1, l2, l3, *_ = sorted(map(len, circuits), reverse=True)
    return l1 * l2 * l3


def solve_08_part_2(file: str) -> int:
    positions = {Position.from_csv(line) for line in file.splitlines()}
    permutations = sorted(
        [(p1, p2) for p1 in positions for p2 in positions if hash(p1) < hash(p2)],
        key=lambda v: v[0].distance_to_sq(v[1]),
    )
    circuits = [{p} for p in positions]
    p1 = Position(0, 0, 0)
    p2 = Position(0, 0, 0)
    for p1, p2 in permutations:
        s1 = next(s for s in circuits if p1 in s)
        s2 = next(s for s in circuits if p2 in s)
        circuits: list[set[Position]] = [s for s in circuits if {p1, p2}.isdisjoint(s)]
        circuits.append(s1.union(s2))
        if len(circuits) <= 1:
            break
    return p1.x * p2.x
