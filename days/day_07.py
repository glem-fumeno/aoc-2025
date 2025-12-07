def solve_part_one(input_file: str):
    beams: set[int] = set()
    splitters: dict[int, set[int]] = {}
    lines = input_file.splitlines()
    for r, line in enumerate(lines):
        splitters[r] = set()
        for c, character in enumerate(line):
            if character == "S":
                beams.add(c)
            elif character == "^":
                splitters[r].add(c)
    split_count = 0
    for row in range(len(lines)):
        nxt = set()
        for beam in beams:
            if beam in splitters[row]:
                split_count += 1
                nxt.add(beam + 1)
                nxt.add(beam - 1)
            else:
                nxt.add(beam)
        beams = nxt
    return split_count


def solve_part_two(input_file: str):
    beams: dict[int, int] = {}
    splitters: dict[int, set[int]] = {}
    lines = input_file.splitlines()
    for r, line in enumerate(lines):
        splitters[r] = set()
        for c, character in enumerate(line):
            if character == "S":
                beams[c] = 1
            elif character == "^":
                splitters[r].add(c)
    for row in range(len(lines)):
        nxt: dict[int, int] = {}
        for beam in beams:
            if beam in splitters[row]:
                nxt[beam + 1] = nxt.get(beam + 1, 0) + beams[beam]
                nxt[beam - 1] = nxt.get(beam - 1, 0) + beams[beam]
            else:
                nxt[beam] = beams[beam] + nxt.get(beam, 0)
        beams = nxt
    return sum(beams.values())
