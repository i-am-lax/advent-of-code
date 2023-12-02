from pathlib import Path
from typing import List


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
