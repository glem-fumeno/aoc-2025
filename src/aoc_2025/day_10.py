import re
from dataclasses import dataclass
from typing import Self

input_pattern = re.compile(
    r"\[([.#]+)\] ((?:\((?:[0-9]+,?)+\) ?)+) \{((?:[0-9]+,?)+)\}"
)


def opposite(light: str) -> str:
    if light == "#":
        return "."
    return "#"


def switch_button(lights: str, button: tuple[int, ...]) -> str:
    return "".join(
        opposite(light) if i in button else light for i, light in enumerate(lights)
    )


def amounted_joltage(
    amounts: tuple[int, ...], buttons: list[tuple[int, ...]], length: int
) -> tuple[int, ...]:
    lights = [0] * length
    for amount, button in zip(amounts, buttons):
        for light in button:
            lights[light] += amount
    return tuple(lights)


@dataclass
class Indicators:
    lights: str
    buttons: list[tuple[int, ...]]
    joltages: tuple[int, ...]

    @property
    def size(self) -> int:
        return len(self.joltages)

    @classmethod
    def from_line(cls, line: str) -> Self:
        m = input_pattern.match(line)
        assert m is not None
        lights, buttons, joltages = m.groups()
        buttons = [
            tuple(map(int, button[1:-1].split(","))) for button in buttons.split(" ")
        ]
        joltages = tuple(map(int, joltages.split(",")))
        return cls(lights, buttons, joltages)

    def lights_out_depth(self) -> int:
        swapped_indices = [(self.lights, 0)]
        seen = {self.lights}
        for lights, depth in swapped_indices:
            if all(light == "." for light in lights):
                return depth
            for button in self.buttons:
                new_lights = switch_button(lights, button)
                if new_lights in seen:
                    continue
                seen.add(new_lights)
                swapped_indices.append((new_lights, depth + 1))
        assert False, "unreachable!"

    def joltage_target_depth(self) -> int:
        depths: list[tuple[tuple[int, ...], int]] = [(tuple([0] * self.size), 0)]
        for amounts, depth in depths:
            amounted = amounted_joltage(amounts, self.buttons, self.size)
        assert False, "unreachable!"


class Solution10:
    def __init__(self, file: str) -> None:
        self.indicators = list(map(Indicators.from_line, file.splitlines()))

    def solve_part_1(self) -> int:
        return sum(indicator.lights_out_depth() for indicator in self.indicators)

    def solve_part_2(self) -> int:
        indicators = self.indicators[0]
        print(amounted_joltage([1, 3, 0, 3, 1, 2], indicators.buttons, 4))
        print(indicators)
        return 0
