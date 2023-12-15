from pathlib import Path


def main():
    input_path = Path("input/input_15.txt")
    print(solve_part_one(input_path))  # 494990 (high)
    print(solve_part_two(input_path))  # 57288 (low)


def hash_string(string: str):
    hash_value = 0
    for char in string:
        hash_value += ord(char)
        hash_value *= 17
        hash_value %= 256
    return hash_value


def parse_input(input_path: Path):
    return tuple(input_path.read_text().strip().split(","))


def initialization_step(instruction, hash_map):
    if "=" in instruction:
        label, focal_length = instruction.split("=")
        label_hash = hash_string(label)
        focal_length = int(focal_length)

        if label_hash not in hash_map:
            hash_map[label_hash] = {}

        hash_map[label_hash][label] = focal_length

    elif "-" in instruction:
        label = instruction.replace("-", "")
        label_hash = hash_string(label)
        if label_hash in hash_map:
            hash_map[label_hash].pop(label, None)
            if not hash_map[label_hash]:
                hash_map.pop(label_hash)

    return hash_map


def solve_part_one(input_path: Path):
    initialization_sequence = parse_input(input_path)
    return sum(map(hash_string, initialization_sequence))


def solve_part_two(input_path: Path):
    initialization_sequence = parse_input(input_path)
    hash_map = {}
    for instruction in initialization_sequence:
        hash_map = initialization_step(instruction, hash_map)

    focusing_power = 0
    for box_number, box in hash_map.items():
        for n, lens in enumerate(box.values(), start=1):
            focusing_power += (box_number + 1) * n * lens
    return focusing_power


if __name__ == "__main__":
    main()
