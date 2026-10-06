from functools import lru_cache


def is_repeated_n(value: str, length: int, n: int) -> bool:
    return value[: length // n] * n == value


def solve_02_part_1(file: str) -> int:
    total = 0
    for low, high in map(lambda v: v.split("-"), file.split(",")):
        if len(low) == len(high) and len(low) % 2 != 0:
            continue
        for number in map(str, range(int(low), int(high) + 1)):
            if len(number) % 2 != 0:
                continue
            if is_repeated_n(number, len(number), 2):
                total += int(number)
    return total


@lru_cache(None)
def divisors(number: int) -> list[int]:
    return [i for i in range(2, number + 1) if number % i == 0]


def solve_02_part_2(file: str) -> int:
    total = 0
    for low, high in map(lambda v: v.split("-"), file.split(",")):
        for number in range(int(low), int(high) + 1):
            digits = str(number)
            length = len(digits)
            for divisor in divisors(length):
                if is_repeated_n(digits, length, divisor):
                    total += number
                    break
    return total
