from collections import defaultdict, namedtuple
from pathlib import Path
from typing import Dict, List, Tuple

CategoryMap = namedtuple("CategoryMap", "destination source length")


def generate_mappings() -> Tuple[List, Dict]:
    filename = "input.txt"
    seeds, maps, current = [], defaultdict(list), None
    with open(Path(__file__).parent / filename, "r") as f:
        for line in f:
            line = line.strip("\n")
            if line.startswith("seeds"):
                seeds = [int(s) for s in line.split(": ")[-1].split()]
                continue
            if line.endswith("map:"):
                current = line.split(" map:")[0]
                continue
            if len(line):
                maps[current].append(CategoryMap(*[int(n) for n in line.split()]))

    return seeds, maps


def apply_category_map(n: int, maps: Dict, name: str) -> int:
    for m in maps[name]:
        difference = n - m.source
        if 0 <= difference < m.length:
            return m.destination + difference
    return n


def get_location(seed: int, maps: Dict) -> int:
    soil_number = apply_category_map(seed, maps, "seed-to-soil")
    fertilizer_number = apply_category_map(soil_number, maps, "soil-to-fertilizer")
    water_number = apply_category_map(fertilizer_number, maps, "fertilizer-to-water")
    light_number = apply_category_map(water_number, maps, "water-to-light")
    temperature_number = apply_category_map(light_number, maps, "light-to-temperature")
    humidity_number = apply_category_map(
        temperature_number, maps, "temperature-to-humidity"
    )
    location_number = apply_category_map(humidity_number, maps, "humidity-to-location")
    return location_number


def main():
    seeds, maps = generate_mappings()
    min_location = None
    for seed in seeds:
        location = get_location(seed, maps)
        if min_location is None:
            min_location = location
        else:
            min_location = min(min_location, location)

    print(f"Minimum location across seeds is: {min_location}")


if __name__ == "__main__":
    main()
