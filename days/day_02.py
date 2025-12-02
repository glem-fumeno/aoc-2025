def solve_part_one(input_file: str):
    count = 0
    for record in input_file.split(","):
        r_start, r_end = record.split("-")
        if len(r_start) == len(r_end) and len(r_end) % 2 == 1:
            continue
        for entry_num in range(int(r_start), int(r_end) + 1):
            entry = str(entry_num)
            el = len(entry)
            if entry[: el // 2] == entry[el // 2 :]:
                count += entry_num
    return count


def solve_part_two(input_file: str):
    count = 0
    for record in input_file.split(","):
        r_start, r_end = map(int, record.split("-"))
        for entry_num in range(r_start, r_end + 1):
            entry = str(entry_num)
            el = len(entry)
            for i in range(1, el // 2 + 1):
                if el % i != 0:
                    continue
                if entry.count(entry[:i]) == el // i:
                    count += entry_num
                    break
    return count
