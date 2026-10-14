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


def increase_button(
    joltages: tuple[int, ...], button: tuple[int, ...]
) -> tuple[int, ...]:
    return tuple(j + 1 if i in button else j for i, j in enumerate(joltages))


@dataclass
class Indicators:
    lights: str
    buttons: list[tuple[int, ...]]
    joltages: tuple[int, ...]

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
        swapped_indices = [(tuple([0] * len(self.joltages)), 0)]
        seen = {tuple([0] * len(self.joltages))}
        for joltages, depth in swapped_indices:
            if all(joltage == self.joltages[i] for i, joltage in enumerate(joltages)):
                return depth
            for button in self.buttons:
                new_joltages = increase_button(joltages, button)
                if new_joltages in seen:
                    continue
                if any(
                    joltage > self.joltages[i] for i, joltage in enumerate(new_joltages)
                ):
                    continue
                seen.add(new_joltages)
                swapped_indices.append((new_joltages, depth + 1))
        assert False, "unreachable!"


class Solution10:
    def __init__(self, file: str) -> None:
        self.indicators = list(map(Indicators.from_line, file.splitlines()))

    def solve_part_1(self) -> int:
        return sum(indicator.lights_out_depth() for indicator in self.indicators)

    def solve_part_2(self) -> int:
        return sum(
            indicator.joltage_target_depth()
            for i, indicator in enumerate(self.indicators)
            if print(i) is None
        )
