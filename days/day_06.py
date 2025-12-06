from functools import reduce
from typing import Literal, get_args

OperatorLiteral = Literal["+", "-", "*", "/"]
OPERATORS = get_args(OperatorLiteral)


def calculate(a: int, op: OperatorLiteral, b: int) -> int:
    match op:
        case "+":
            return a + b
        case "-":
            return a - b
        case "*":
            return a * b
        case "/":
            return a // b


def solve_part_one(input_file: str):
    lines = input_file.splitlines()
    operators: list = [op for op in lines[-1] if op in OPERATORS]
    numbers = [[int(n) for n in l.split(" ") if n != ""] for l in lines[:-1]]
    results, *numbers = numbers
    for row in numbers:
        for i, number in enumerate(row):
            results[i] = calculate(results[i], operators[i], number)
    return sum(results)


def solve_part_two(input_file: str):
    lines = input_file.splitlines()
    operators: list = [op for op in lines[-1] if op in OPERATORS]
    number_inputs = ["" for _ in input_file.splitlines()[0]]
    for line in lines[:-1]:
        for i, number in enumerate(line):
            if number != " ":
                number_inputs[i] += number
    numbers = [[]]
    for number in number_inputs:
        if number == "":
            numbers.append([])
        else:
            numbers[-1].insert(0, int(number))
    return sum(
        reduce(lambda a, b: calculate(a, op, b), numbers)
        for numbers, op in zip(numbers, operators)
    )
