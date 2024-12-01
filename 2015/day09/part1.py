import operator
import re
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

distances = {}
for line in data_raw:
    source, destination, distance = re.match(r"(\w+) to (\w+) = (\d+)", line).groups()
    if source not in distances:
        distances[source] = []
    if destination not in distances:
        distances[destination] = []
    distances[source].append((destination, int(distance)))
    distances[destination].append((source, int(distance)))


def find_shortest_path(current_path=tuple(), current_length=0) -> tuple[list[str], int]:
    possible_next = tuple(
        zip(distances.keys(), [0] * len(distances))
        if not current_path
        else distances.get(current_path[-1], [])
    )
    possible_next = tuple(
        (destination, length)
        for destination, length in possible_next
        if destination not in current_path
    )
    if not possible_next:
        return current_path, current_length

    paths = [
        find_shortest_path(current_path + (destination,), current_length + length)
        for destination, length in possible_next
    ]
    return min(paths, key=operator.itemgetter(1))


print(find_shortest_path()[1])
