from functools import lru_cache


def is_repeated_n(value: str, length: int, n: int) -> bool:
    return value[: length // n] * n == value


@lru_cache(None)
def divisors(number: int) -> list[int]:
    return [i for i in range(2, number + 1) if number % i == 0]


class Solution02:
    def __init__(self, file: str) -> None:
        self.ranges = list(map(lambda v: v.split("-"), file.split(",")))

    def solve_part_1(self) -> int:
        total = 0
        for low, high in self.ranges:
            if len(low) == len(high) and len(low) % 2 != 0:
                continue
            for number in map(str, range(int(low), int(high) + 1)):
                if len(number) % 2 != 0:
                    continue
                if is_repeated_n(number, len(number), 2):
                    total += int(number)
        return total

    def solve_part_2(self) -> int:
        total = 0
        for low, high in self.ranges:
            for number in range(int(low), int(high) + 1):
                digits = str(number)
                length = len(digits)
                for divisor in divisors(length):
                    if is_repeated_n(digits, length, divisor):
                        total += number
                        break
        return total
