def max_substr(digits: str, depth: int) -> str:
    if depth < 1:
        return ""
    max_i, max_digit = 0, "0"
    for i in range(len(digits) - depth + 1):
        if digits[i] > max_digit:
            max_digit, max_i = digits[i], i
    return max_digit + max_substr(digits[max_i + 1 :], depth - 1)


class Solution03:
    def __init__(self, file: str) -> None:
        self.banks = file.splitlines()

    def solve_part_1(self) -> int:
        return sum(int(max_substr(line, 2)) for line in self.banks)

    def solve_part_2(self) -> int:
        return sum(int(max_substr(line, 12)) for line in self.banks)
