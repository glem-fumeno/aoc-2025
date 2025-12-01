def solve_part_one(input_file: str):
    count = 0
    dial = 50
    for line in input_file.splitlines():
        direction, *magnitude = line
        magnitude = int("".join(magnitude))
        match direction:
            case "R":
                dial += magnitude
            case "L":
                dial -= magnitude
        dial %= 100
        if dial == 0:
            count += 1
    return count


def solve_part_two(input_file: str):
    count = 0
    dial = 50
    for line in input_file.splitlines():
        direction, *magnitude = line
        magnitude = int("".join(magnitude))
        for _ in range(magnitude):
            match direction:
                case "R":
                    dial += 1
                case "L":
                    dial -= 1
            dial %= 100
            if dial == 0:
                count += 1
    return count
