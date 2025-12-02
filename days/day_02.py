def solve_part_one(input_file: str):
    count = 0
    for record in input_file.split(","):
        r_start, r_end = map(int, record.split("-"))
        if len(str(r_start)) == len(str(r_end)) and len(str(r_end)) % 2 == 1:
            continue
        for entry_num in range(r_start, r_end + 1):
            entry = str(entry_num)
            if len(entry) % 2 == 1:
                continue
            pivot = len(entry) // 2
            if entry[:pivot] == entry[pivot:]:
                count += entry_num
    return count


def solve_part_two(input_file: str):
    count = 0
    for record in input_file.split(","):
        r_start, r_end = map(int, record.split("-"))
        for entry_num in range(r_start, r_end + 1):
            entry = str(entry_num)
            for i in range(len(entry) // 2):
                if len(entry) / (i + 1) % 1 != 0:
                    continue
                if entry.count(entry[: i + 1]) == len(entry) / (i + 1):
                    count += entry_num
                    break
    return count
