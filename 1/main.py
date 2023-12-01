from pathlib import Path
from typing import List


def read_file_into_list(filename: Path, delimiter: str = "\n") -> List:
    """
    Read file into list.
    """
    file = open(filename, "r")
    data = file.read().split(delimiter)
    file.close()
    return data


def get_sum_of_calibration_values(data: List) -> int:
    """
    Compute sum of the calibration values by combining the first
    and last digit to form a single two-digit number.
    """
    # initialise total sum and variables to store first and last digits
    sum = 0
    first, last = None, None

    # iterate through calibration values in the input
    for value in data:
        # iterate through each letter and determine whether it is a digit or not
        for letter in value:
            if letter.isdigit():
                if first is None:
                    first = letter
                else:
                    last = letter
        if last is None:
            last = first

        # increase sum
        sum += int(first + last)

        # reset values
        first, last = None, None

    return sum


def main():
    # read input file
    data = read_file_into_list(Path("input.txt"))

    # calculate sum of calibration values
    sum = get_sum_of_calibration_values(data)
    print(f"Total sum of calibration values: {sum}")


if __name__ == "__main__":
    main()
