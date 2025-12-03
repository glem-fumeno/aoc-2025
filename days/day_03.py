def max_of_width(line: str, width: int):
    start = 0
    end = len(line) - width + 1
    result = ""
    while len(result) < width:
        result += max(line[start : end + len(result)])
        start = line.index(result[-1], start) + 1
    return int(result)


def solve_part_one(input_file: str):
    return sum(max_of_width(l, 2) for l in input_file.splitlines())


def solve_part_two(input_file: str):
    return sum(max_of_width(l, 12) for l in input_file.splitlines())
