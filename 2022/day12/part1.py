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


# Dijkstra
unvisited = set(range(len(data1D)))

shortest_distance = defaultdict(lambda: float("inf"))
shortest_distance[start] = 0

queue = PriorityQueue()
queue.put((0, start))

while True:
    _, current = queue.get()
    if current == end:
        print(shortest_distance[end])
        break

    if current not in unvisited:
        continue
    current_elevation = ord(data1D[current])
    current_distance = shortest_distance[current]
    for neighbor_pos in get_neighbor_positions(current):
        neighbor_elevation = ord(data1D[neighbor_pos])
        if neighbor_elevation > 1 + current_elevation:
            continue
        shortest_distance[neighbor_pos] = min(
            shortest_distance[neighbor_pos], current_distance + 1
        )
        queue.put((shortest_distance[neighbor_pos], neighbor_pos))
    unvisited.remove(current)
