from functools import reduce
from typing import Literal, cast

type OperationLiteral = Literal["*", "+"]


def execute(operation: OperationLiteral, values: list[int]) -> int:
    match operation:
        case "*":
            return reduce(lambda a, b: a * b, values, 1)
        case "+":
            return sum(values)


class Solution06:
    def __init__(self, file: str) -> None:
        self.file = file

    def solve_part_1(self) -> int:
        *numbers, symbols = self.file.splitlines()
        operations = cast(list[OperationLiteral], [s for s in symbols if s != " "])
        equations: list[list[int]] = [[] for _ in operations]
        for line in numbers:
            for i, number in enumerate([n for n in line.split(" ") if n != ""]):
                equations[i].append(int(number))
        return sum(map(execute, operations, equations))

    def solve_part_2(self) -> int:
        equations: list[list[int]] = [[]]
        operations: list[OperationLiteral] = []
        for elements in zip(*self.file.splitlines()):
            if all(e == " " for e in elements):
                equations.append([])
                continue
            *values, operation = elements
            if operation != " ":
                operations.append(cast(OperationLiteral, operation))
            equations[-1].append(int("".join(values).strip()))
        return sum(map(execute, operations, equations))
