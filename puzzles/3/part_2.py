"""
test.txt - 467835
test_2.txt - 6756
test_3.txt - 925
"""
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import List

import numpy as np


@dataclass(unsafe_hash=True)
class Part:
    number: int
    row_idx: int
    min_col_idx: int
    max_col_idx: int


def parse_input_as_array(filename: str) -> np.array:
    data = []
    with open(Path(__file__).parent / filename, "r") as file:
        for line in file:
            data.append([val for val in line.strip()])
    array = np.array(data)
    return array


def _get_parts(array: np.array) -> List:
    """
    List of all the parts with their index ranges.
    """
    parts, part, start_col_idx = [], "", None

    def _add_part(row_idx, end_col_idx):
        if part:
            parts.append(Part(int(part), row_idx, start_col_idx, end_col_idx))
            return "", None
        return part, start_col_idx

    for row_idx in range(array.shape[0]):
        for col_idx in range(array.shape[1]):
            # construct part number and record start index
            character = array[row_idx][col_idx]
            if character.isdigit():
                if not part:
                    start_col_idx = col_idx
                part += character
            else:
                part, start_col_idx = _add_part(row_idx, col_idx - 1)

        # handle case where part number extends to the end of a row
        part, start_col_idx = _add_part(row_idx, array.shape[1] - 1)

    return parts


def _generate_adjacent_coordinates(row_idx: int, col_idx: int) -> List:
    return [
        (row_idx + row_delta, col_idx + col_delta)
        for row_delta in range(-1, 2)
        for col_delta in range(-1, 2)
        if not (row_delta == 0 and col_delta == 0)
    ]


def _get_gear_ratio(row_idx, col_idx, parts: List[Part]) -> int:
    # coordinates adjacent to gear
    adjacent_coordinates = _generate_adjacent_coordinates(row_idx, col_idx)

    # find adjacent parts
    adjacent_parts = set()
    for coordinates in adjacent_coordinates:
        for part in parts:
            if (
                part.row_idx == coordinates[0]
                and part.min_col_idx <= coordinates[1] <= part.max_col_idx
            ):
                adjacent_parts.add(part)

    # for exactly two adjacent parts, multiply the numbers
    gear_ratio = 0
    if len(adjacent_parts) == 2:
        gear_ratio = reduce(lambda x, y: x.number * y.number, adjacent_parts)

    return gear_ratio


def get_sum_of_gear_ratios(array: np.array) -> int:
    """
    Total sum of gear ratios for schematic.
    """
    # identify all of the parts
    parts = _get_parts(array)
    print(f"Length of parts: {len(parts)}")

    sum = 0
    for row_idx in range(array.shape[0]):
        for col_idx in range(array.shape[1]):
            if array[row_idx][col_idx] == "*":
                sum += _get_gear_ratio(row_idx, col_idx, parts)

    return sum


def main():
    # read input into array
    schematic = parse_input_as_array("input.txt")
    print(f"Size of engine schematic: {schematic.shape}")

    # compute sum of gear ratios
    sum_of_gear_ratios = get_sum_of_gear_ratios(schematic)
    print(f"Sum of gear ratios: {sum_of_gear_ratios}")


if __name__ == "__main__":
    main()
