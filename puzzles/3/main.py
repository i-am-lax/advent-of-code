import string
from pathlib import Path

import numpy as np


def parse_input_as_array(filename: str = "test.txt") -> np.array:
    data = []
    with open(Path(__file__).parent / filename, "r") as file:
        for line in file:
            data.append([val for val in line.strip()])
    array = np.array(data)
    return array


def is_symbol_adjacent(row_idx: int, col_idx: int, array: np.array) -> bool:
    symbols = string.punctuation.replace(".", "")
    adjacent_coordinates = [
        (row_idx + row_delta, col_idx + col_delta)
        for row_delta in range(-1, 2)
        for col_delta in range(-1, 2)
        if not (row_delta == 0 and col_delta == 0)
    ]
    is_adjacent = False
    for coordinate in adjacent_coordinates:
        try:
            character = array[coordinate[0]][coordinate[1]]
            if character in symbols:
                is_adjacent = True
        except:
            continue
    return is_adjacent


def get_sum_of_parts(array: np.array) -> int:
    sum = 0
    part = ""
    is_adjacent = False
    for row_idx in range(array.shape[0]):
        for col_idx in range(array.shape[1]):
            character = array[row_idx][col_idx]
            if character.isdigit():
                part += character
                if not is_adjacent:
                    is_adjacent = is_symbol_adjacent(row_idx, col_idx, array)
            else:
                if len(part) > 0:
                    sum += int(part) * is_adjacent
                part = ""
                is_adjacent = False
    return sum


def main():
    # read input into array
    schematic = parse_input_as_array("input.txt")
    print(f"Size of engine schematic: {schematic.shape}")

    # sum of parts adjacent to symbol
    sum_of_parts = get_sum_of_parts(schematic)
    print(f"Sum of parts: {sum_of_parts}")


if __name__ == "__main__":
    main()
