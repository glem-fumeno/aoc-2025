def solve_part_one(input_file: str):
    count = 0
    fresh_ranges = []
    analyzing_freshness = True
    for line in input_file.splitlines():
        if line == "":
            analyzing_freshness = False
            continue
        if analyzing_freshness:
            fresh_ranges.append(tuple(map(int, line.split("-"))))
        else:
            if any(ge <= int(line) <= le for ge, le in fresh_ranges):
                count += 1
    return count


def solve_part_two(input_file: str):
    fresh_ranges = set()

    def in_conflict(ge: int, le: int, gec: int, lec: int):
        return ge <= gec <= le or ge <= lec <= le

    for line in input_file.splitlines():
        if line == "":
            break
        ge, le = map(int, line.split("-"))
        conflicts = {
            (gec, lec)
            for gec, lec in fresh_ranges
            if in_conflict(ge, le, gec, lec) or in_conflict(gec, lec, ge, le)
        }
        min_ge = min({ge, *(map(lambda x: x[0], conflicts))})
        max_le = max({le, *(map(lambda x: x[1], conflicts))})
        fresh_ranges.difference_update(conflicts)
        fresh_ranges.add((min_ge, max_le))
    return sum((le - ge + 1) for ge, le in fresh_ranges)
