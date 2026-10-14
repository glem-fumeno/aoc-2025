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


class Solution01:
    def __init__(self, file: str) -> None:
        self.dials = [get_dial(line) for line in file.splitlines()]

    def solve_part_1(self) -> int:
        dial = 50
        solution = 0
        for direction, magnitude in self.dials:
            dial = get_rotated_dial(dial, direction, magnitude) % 100
            if dial == 0:
                solution += 1
        return solution

    def solve_part_2(self) -> int:
        dial = 50
        solution = 0
        for direction, magnitude in self.dials:
            solution += (magnitude - magnitude % 100) // 100
            new_dial = get_rotated_dial(dial, direction, magnitude % 100)
            if dial != 0 and not (0 < new_dial < 100):
                solution += 1
            dial = new_dial % 100
        return solution
