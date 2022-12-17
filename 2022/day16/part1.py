import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from queue import PriorityQueue, Queue
from typing import Iterator

data = Path(__file__).with_name("input.txt").read_text().splitlines()
steps_limit = 30

# parse data
flow_rates: dict[str, int] = {}
neighbors: dict[str, list[str]] = {}
for line in data:
    match = re.match(r"Valve (\w+) .*=(\d+); .* valves? (.+)", line)
    valve = match[1]
    flow_rates[valve] = int(match[2])
    neighbors[valve] = match[3].split(", ")

# precompute stuff
valves = set(flow_rates.keys())
openable_valves = set(valve for valve, rate in flow_rates.items() if rate > 0)
# distances between valves
distances: dict[tuple[str, str], int] = defaultdict(lambda: float("inf"))
for source, targets in neighbors.items():
    distances[(source, source)] = 0
    for target in targets:
        distances[(source, target)] = 1
for k in valves:
    for i in valves:
        for j in valves:
            dist_via_k = distances[(i, k)] + distances[(k, j)]
            if distances[(i, j)] > dist_via_k:
                distances[(i, j)] = dist_via_k


@dataclass
class State:
    # uniqueness of the state
    current_pos: str
    open_valves: set[str]

    # not unique, only used for stopping
    minutes_passed: int

    def __hash__(self) -> int:
        return hash((self.current_pos, tuple(sorted(self.open_valves))))

    def __lt__(self, other) -> bool:
        return hash(self) < hash(other)


def reachable_states(state: State) -> Iterator[tuple[State, int]]:
    current_flow = sum(flow_rates[valve] for valve in state.open_valves)

    # wait and do nothing until the end
    steps_left = steps_limit - state.minutes_passed
    yield (
        State(
            current_pos=state.current_pos,
            open_valves=state.open_valves,
            minutes_passed=state.minutes_passed + steps_left,
        ),
        -current_flow * steps_left,
    )

    # move to other unopened valve and open it
    for other in openable_valves - state.open_valves:
        dist = distances[(state.current_pos, other)]
        yield (
            State(
                current_pos=other,
                open_valves=state.open_valves | {other},
                minutes_passed=state.minutes_passed + dist + 1,
            ),
            -current_flow * (dist + 1),
        )


# admissable heuristic for A*
def min_cost_to_end(state: State) -> int:
    # cost = -gains
    # never overestimate cost = never underestimate gains
    # assume best possible way to open all remaining valves
    steps_left = steps_limit - state.minutes_passed
    max_gains = 0
    # all currently open valves continue to flow
    max_gains += steps_left * sum(flow_rates[valve] for valve in state.open_valves)
    # assume we can reach and open each other valve in it's minimum distance
    remaining_valves = openable_valves - state.open_valves
    for valve in remaining_valves:
        dist = distances[(state.current_pos, valve)]
        if dist < steps_left - 1:
            max_gains += (steps_left - dist - 1) * flow_rates[valve]

    return -max_gains


# A* implementation to search the space
start: State = State(
    current_pos="AA",
    open_valves=set(),
    minutes_passed=0,
)
q: Queue[tuple[int, State]] = PriorityQueue()
q.put((0, start))

cheapest_path_from_start: dict[State, int] = defaultdict(lambda: float("inf"))
cheapest_path_from_start[start] = 0

while not q.empty():
    cost, current = q.get()

    if current.minutes_passed == steps_limit:
        print(-cost)
        break

    for neighbor, transition_cost in reachable_states(current):
        tentative_score = cheapest_path_from_start[current] + transition_cost
        if tentative_score < cheapest_path_from_start[neighbor]:
            cheapest_path_from_start[neighbor] = tentative_score
            cost_estimate = tentative_score + min_cost_to_end(neighbor)
            q.put((cost_estimate, neighbor))
