from functools import reduce
from typing import Literal, cast

type OperationLiteral = Literal["*", "+"]


def execute(operation: OperationLiteral, values: list[int]) -> int:
    match operation:
        case "*":
            return reduce(lambda a, b: a * b, values, 1)
        case "+":
            return sum(values)


def solve_06_part_1(file: str) -> int:
    *numbers, symbols = file.splitlines()
    operations = cast(list[OperationLiteral], [s for s in symbols if s != " "])
    equations: list[list[int]] = [[] for _ in operations]
    for line in numbers:
        for i, number in enumerate([n for n in line.split(" ") if n != ""]):
            equations[i].append(int(number))
    return sum(map(execute, operations, equations))


def solve_06_part_2(file: str) -> int:
    equations: list[list[int]] = [[]]
    operations: list[OperationLiteral] = []
    for elements in zip(*file.splitlines()):
        if all(e == " " for e in elements):
            equations.append([])
            continue
        *values, operation = elements
        if operation != " ":
            operations.append(cast(OperationLiteral, operation))
        equations[-1].append(int("".join(values).strip()))
    return sum(map(execute, operations, equations))
