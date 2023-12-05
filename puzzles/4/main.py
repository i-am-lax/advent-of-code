import re
from pathlib import Path


def main():
    total_points = 0

    filename = "input.txt"
    with open(Path(__file__).parent / filename, "r") as f:
        for line in f:
            numbers = re.sub("Card \d+: ", "", line.strip())
            winning, current = map(str.split, numbers.split("|"))
            matches = set(winning) & set(current)
            if matches:
                total_points += 2 ** (len(matches) - 1)

    print(f"Total points: {total_points}")


if __name__ == "__main__":
    main()
