class FreshRange:
    min: int
    max: int

    def __init__(self, min: int, max: int) -> None:
        self.min = min
        self.max = max

    def merge(self, other: FreshRange):
        self.min = min(self.min, other.min)
        self.max = max(self.max, other.max)

    def intersects(self, other: FreshRange) -> bool:
        return (
            False
            or self.min in other
            or self.max in other
            or other.min in self
            or other.max in self
        )

    def span(self) -> int:
        return self.max - self.min + 1

    def __contains__(self, other: int) -> bool:
        return self.min <= other <= self.max

    def __hash__(self) -> int:
        return hash((self.min, self.max))


def solve_05_part_1(file: str) -> int:
    ranges: list[FreshRange] = []
    ranges_file, produce_file = file.split("\n\n")
    for r in ranges_file.splitlines():
        ranges.append(FreshRange(*map(int, r.split("-"))))
    total = 0
    for produce in produce_file.splitlines():
        total += any(int(produce) in fresh_range for fresh_range in ranges)
    return total


def solve_05_part_2(file: str) -> int:
    ranges: list[FreshRange] = []
    ranges_file, _ = file.split("\n\n")
    for fresh_range in ranges_file.splitlines():
        new_range = FreshRange(*map(int, fresh_range.split("-")))
        to_pop: set[int] | None = None
        while to_pop is None or len(to_pop) > 0:
            to_pop = set()
            for i, fresh_range in enumerate(ranges):
                if fresh_range.intersects(new_range):
                    new_range.merge(fresh_range)
                    to_pop.add(i)
            ranges = [r for i, r in enumerate(ranges) if i not in to_pop]
        ranges.append(new_range)
    return sum(r.span() for r in ranges)
