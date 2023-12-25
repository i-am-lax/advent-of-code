import re
from collections import defaultdict
from pathlib import Path


def main():
    total_points = 0
    cards = defaultdict(int)
    filename = "input.txt"

    with open(Path(__file__).parent / filename, "r") as f:
        for line in f:
            line = line.strip()
            card_number = int(re.search(r"Card\s+(\d+)", line).group(1))

            # count original scratch card
            cards[card_number] += 1

            # compute winning numbers
            numbers = re.sub("Card \d+: ", "", line.strip())
            winning, current = map(str.split, numbers.split("|"))
            matches = len(set(winning) & set(current))
            if matches:
                total_points += 2 ** (matches - 1)

            # add count to cards
            for c in range(card_number + 1, card_number + matches + 1):
                multiplier = cards[card_number]
                cards[c] += multiplier

    total_cards = sum(cards.values())

    print(f"Total points: {total_points}")
    print(f"Total cards: {total_cards}")


if __name__ == "__main__":
    main()
