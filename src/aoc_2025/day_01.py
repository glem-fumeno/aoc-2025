from typing import Literal, cast

type DirectionLiteral = Literal["L", "R"]


def get_dial(line: str) -> tuple[DirectionLiteral, int]:
    direction, *magnitude = line
    return cast(DirectionLiteral, direction), int("".join(magnitude))


def get_rotated_dial(dial: int, direction: DirectionLiteral, magnitude: int) -> int:
    match direction:
        case "L":
            return dial - magnitude
        case "R":
            return dial + magnitude


def solve_01_part_1(file: str) -> int:
    dial = 50
    solution = 0
    for line in file.splitlines():
        dial = get_rotated_dial(dial, *get_dial(line)) % 100
        if dial == 0:
            solution += 1
    return solution


def solve_01_part_2(file: str) -> int:
    dial = 50
    solution = 0
    for line in file.splitlines():
        direction, magnitude = get_dial(line)
        solution += (magnitude - magnitude % 100) // 100
        new_dial = get_rotated_dial(dial, direction, magnitude % 100)
        if dial != 0 and not (0 < new_dial < 100):
            solution += 1
        dial = new_dial % 100
    return solution
