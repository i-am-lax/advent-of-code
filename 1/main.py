import re
from pathlib import Path
from typing import List


WORD_TO_DIGIT = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def read_file_into_list(file_path: Path) -> List:
    """
    Read lines from file into list.

    Args:
        file_path (Path): Path to input file.
    Returns:
        List: List of strings representing new-line separated lines from file.
    """
    file = open(file_path, "r")
    data = file.read().split("\n")
    file.close()
    return data


def find_digits(input: str) -> List:
    """
    Identify any digit character or word in the input string.

    Args:
        input (str): Input string.
    Returns:
        List containing identified digits (if any).
    """
    # by default finds non-overlapping matches so we need lookahead assertion
    pattern = r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))"
    return re.findall(pattern, input)


def get_sum_of_calibration_values(data: List) -> int:
    """
    Compute sum of the calibration values by combining the first
    and last digit to form a single two-digit number.
    28gtbkszmrtmnineoneightmx -> 28
    4xj -> 44
    ninefourone1 -> 91

    Args:
        data (List): Calibration values.
    Returns:
        int: Sum of the calibration values.
    """
    # initialise total sum
    sum = 0

    # convert word to digit
    convert_word_to_digit = lambda d: WORD_TO_DIGIT.get(d, d)

    # iterate through calibration values in the input
    for value in data:
        # identify digit characters / words using regex pattern
        digits = find_digits(value)

        # increase sum with first and last digits
        if digits:
            first = convert_word_to_digit(digits[0])
            last = convert_word_to_digit(digits[-1])
            sum += int(first + last)

    return sum


def main():
    # read input file
    data = read_file_into_list(Path("input.txt"))

    # calculate sum of calibration values
    sum = get_sum_of_calibration_values(data)
    print(f"Total sum of calibration values: {sum}")


if __name__ == "__main__":
    main()
