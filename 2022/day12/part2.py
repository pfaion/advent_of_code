from collections import defaultdict
from pathlib import Path
from queue import PriorityQueue

data = Path(__file__).with_name("input.txt").read_text().splitlines()

cols = len(data[0])
data1D = "".join(data)
start = data1D.find("S")
end = data1D.find("E")
data1D = data1D.replace("S", "a").replace("E", "z")


def get_neighbor_positions(pos: int) -> set[int]:
    neighbor_positions = set()
    if (pos % cols) > 0:  # left
        neighbor_positions.add(pos - 1)
    if (pos % cols) < cols - 1:  # right
        neighbor_positions.add(pos + 1)
    if pos > cols:  # up
        neighbor_positions.add(pos - cols)
    if pos < len(data1D) - cols:  # down
        neighbor_positions.add(pos + cols)
    return neighbor_positions


# Dijkstra reversed:
# search all paths from the end until we have hit all reachable "a"s
unvisited = set(range(len(data1D)))
possible_starts = set(i for i, elevation in enumerate(data1D) if elevation == "a")
unvisited_starts = possible_starts.copy()

shortest_distance = defaultdict(lambda: float("inf"))
shortest_distance[end] = 0

queue = PriorityQueue()
queue.put((0, end))

while True:
    if not unvisited_starts or queue.empty():
        print(min(shortest_distance[i] for i in possible_starts))
        break

    _, current = queue.get()
    if current not in unvisited:
        continue
    current_elevation = ord(data1D[current])
    current_distance = shortest_distance[current]
    for neighbor_pos in get_neighbor_positions(current):
        neighbor_elevation = ord(data1D[neighbor_pos])
        if neighbor_elevation < current_elevation - 1:
            continue
        shortest_distance[neighbor_pos] = min(
            shortest_distance[neighbor_pos], current_distance + 1
        )
        queue.put((shortest_distance[neighbor_pos], neighbor_pos))
    unvisited.remove(current)
    unvisited_starts -= {current}
