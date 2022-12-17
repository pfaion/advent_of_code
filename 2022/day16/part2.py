import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from queue import PriorityQueue, Queue
from typing import Iterator

data = Path(__file__).with_name("input.txt").read_text().splitlines()
steps_limit = 27

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


@dataclass(frozen=True)
class State:
    own_actions: tuple[str]
    own_position: str
    own_target: str
    ele_actions: tuple[str]
    ele_position: str
    ele_target: str
    open_valves: set[str]
    minutes_passed: int
    accumulated_flow: int

    def __hash__(self) -> int:
        return hash(
            (
                self.own_actions,
                self.own_position,
                self.own_target,
                self.ele_actions,
                self.ele_position,
                self.ele_target,
                tuple(sorted(openable_valves)),
            )
        )


def advance_state(state: State) -> State:
    while not (
        state.own_target == ""
        or state.ele_target == ""
        or state.minutes_passed == steps_limit
    ):
        own_reached = len(state.own_actions) == state.minutes_passed
        ele_reached = len(state.ele_actions) == state.minutes_passed
        new_open_valves = state.open_valves.copy()
        if own_reached and state.own_actions[-1] == "open":
            new_open_valves.add(state.own_actions[-2])
        if ele_reached and state.ele_actions[-1] == "open":
            new_open_valves.add(state.ele_actions[-2])

        # this specifically is based on the previously opened valves
        current_flow = sum(flow_rates[valve] for valve in state.open_valves)

        state = State(
            own_actions=state.own_actions,
            own_position=state.own_target if own_reached else "...",
            own_target="" if own_reached else state.own_target,
            ele_actions=state.ele_actions,
            ele_position=state.ele_target if ele_reached else "...",
            ele_target="" if ele_reached else state.ele_target,
            open_valves=new_open_valves,
            minutes_passed=state.minutes_passed + 1,
            accumulated_flow=state.accumulated_flow + current_flow,
        )
    return state


def reachable_states(state: State) -> Iterator[tuple[State, int]]:
    remaining_valves = (openable_valves - state.open_valves) - {
        target for target in (state.own_target, state.ele_target) if target != "noop"
    }
    steps_left = steps_limit - state.minutes_passed

    if state.own_target == "" and state.ele_target == "":
        assert state.own_position in valves
        assert state.ele_position in valves
        for own_target in remaining_valves | {"noop"}:
            own_distance = distances[(state.own_position, own_target)]
            if own_target == "noop":
                new_own_actions = ("noop",) * steps_left
            else:
                new_own_actions = ("...",) * (own_distance - 1) + (own_target, "open")
            for ele_target in (remaining_valves - {own_target}) | {"noop"}:
                ele_distance = distances[(state.ele_position, ele_target)]
                if ele_target == "noop":
                    new_ele_actions = ("noop",) * steps_left
                else:
                    new_ele_actions = ("...",) * (ele_distance - 1) + (
                        ele_target,
                        "open",
                    )
                new_state = State(
                    own_actions=state.own_actions + new_own_actions,
                    own_position=state.own_position,
                    own_target=own_target,
                    ele_actions=state.ele_actions + new_ele_actions,
                    ele_position=state.ele_position,
                    ele_target=ele_target,
                    open_valves=state.open_valves,
                    minutes_passed=state.minutes_passed,
                    accumulated_flow=state.accumulated_flow,
                )
                new_state = advance_state(new_state)
                transition_cost = -(new_state.accumulated_flow - state.accumulated_flow)
                yield new_state, transition_cost
    elif state.own_target == "":
        assert state.own_position in valves
        for own_target in remaining_valves | {"noop"}:
            own_distance = distances[(state.own_position, own_target)]
            if own_target == "noop":
                new_own_actions = ("noop",) * steps_left
            else:
                new_own_actions = ("...",) * (own_distance - 1) + (own_target, "open")
            new_state = State(
                own_actions=state.own_actions + new_own_actions,
                own_position=state.own_position,
                own_target=own_target,
                ele_actions=state.ele_actions,
                ele_position=state.ele_position,
                ele_target=state.ele_target,
                open_valves=state.open_valves,
                minutes_passed=state.minutes_passed,
                accumulated_flow=state.accumulated_flow,
            )
            new_state = advance_state(new_state)
            transition_cost = -(new_state.accumulated_flow - state.accumulated_flow)
            yield new_state, transition_cost
    elif state.ele_target == "":
        assert state.ele_position in valves
        for ele_target in remaining_valves | {"noop"}:
            ele_distance = distances[(state.ele_position, ele_target)]
            if ele_target == "noop":
                new_ele_actions = ("noop",) * steps_left
            else:
                new_ele_actions = ("...",) * (ele_distance - 1) + (ele_target, "open")
            new_state = State(
                own_actions=state.own_actions,
                own_position=state.own_position,
                own_target=state.own_target,
                ele_actions=state.ele_actions + new_ele_actions,
                ele_position=state.ele_position,
                ele_target=ele_target,
                open_valves=state.open_valves,
                minutes_passed=state.minutes_passed,
                accumulated_flow=state.accumulated_flow,
            )
            new_state = advance_state(new_state)
            transition_cost = -(new_state.accumulated_flow - state.accumulated_flow)
            yield new_state, transition_cost


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
        own_pos = (
            state.own_position if state.own_position != "..." else state.own_target
        )
        own_dist = distances[(own_pos, valve)] + (
            len(state.own_actions) - state.minutes_passed
        )
        ele_pos = (
            state.ele_position if state.ele_position != "..." else state.ele_target
        )
        ele_dist = distances[(ele_pos, valve)] + (
            len(state.ele_actions) - state.minutes_passed
        )
        # plus one because we still need to open
        dist = min((own_dist, ele_dist)) + 1
        if dist < steps_left:
            max_gains += (steps_left - dist) * flow_rates[valve]

    return -max_gains


# A* implementation to search the space
start = State(
    own_actions=tuple(),
    own_position="AA",
    own_target="",
    ele_actions=tuple(),
    ele_position="AA",
    ele_target="",
    open_valves=set(),
    minutes_passed=0,
    accumulated_flow=0,
)


@dataclass
class QueueItem:
    prio: int
    state: State

    def __lt__(self, other: "QueueItem") -> bool:
        if self.prio != other.prio:
            return self.prio < other.prio
        return hash(self.state) < hash(other.state)


q: Queue[QueueItem] = PriorityQueue()
q.put(QueueItem(0, start))

cheapest_path_from_start: dict[State, int] = defaultdict(lambda: float("inf"))
cheapest_path_from_start[start] = 0

visited_neighbors = set()

while not q.empty():
    item = q.get()
    cost = item.prio
    current = item.state

    if current.minutes_passed == steps_limit:
        print(-cost)
        break

    for neighbor, transition_cost in reachable_states(current):
        tentative_score = cheapest_path_from_start[current] + transition_cost
        if tentative_score < cheapest_path_from_start[neighbor]:
            visited_neighbors.add(neighbor)
            cheapest_path_from_start[neighbor] = tentative_score
            cost_estimate = tentative_score + min_cost_to_end(neighbor)
            q.put(QueueItem(cost_estimate, neighbor))
