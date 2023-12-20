import re
from collections import defaultdict
from copy import deepcopy
from itertools import count
from pathlib import Path

from rich import print

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

type ModName = str
type ModType = str

# parse data
outgoing: dict[ModName, list[ModName]] = defaultdict(list)
incoming: dict[ModName, list[ModName]] = defaultdict(list)
types: dict[ModName, ModType] = defaultdict(
    lambda: None, **{"broadcaster": "broadcaster"}
)
for line in data_raw:
    type_str, name = re.match(r"([%&]?)(\w+) ->", line).groups()
    connections = re.findall(r"(?:->|,) (\w+)", line)
    if type_str != "":
        types[name] = type_str
    else:
        assert name == "broadcaster"
    outgoing[name].extend(connections)
    for con in connections:
        incoming[con].append(name)

# compute reachable nodes, for cycle detection
transitive_connections: dict[ModName, set[ModName]] = defaultdict(set)
stack = [("broadcaster",)]
while stack and (path := stack.pop()):
    for out in outgoing[path[-1]]:
        for node in path:
            transitive_connections[node].add(out)
        # need to make sure we catch the full cycle at least once
        if path.count(out) < 2:
            stack.append(path + (out,))

# find subsystems, i.e. closed loop systems
type Subsystem = frozenset[ModName]
subsystems: list[Subsystem] = []
for node, reachable in transitive_connections.items():
    is_cycle = node in reachable
    if not is_cycle:
        continue
    result = set()
    for candidate in reachable:
        if node in transitive_connections.get(candidate, set()):
            result.add(candidate)
    subsystems.append(frozenset(result))
subsystems = list(set(subsystems))

# find subsystem inputs
subsystem_inputs = {
    subsystem: frozenset(
        name
        for name, connections in outgoing.items()
        if name not in subsystem and any(part in connections for part in subsystem)
    )
    for subsystem in subsystems
}
if any(inputs != {"broadcaster"} for inputs in subsystem_inputs.values()):
    # if subsystems only depend on broadcaster, they always receive the same input ("low")
    raise NotImplementedError

# find subsystem outputs
subsystem_outputs = {
    subsystem: frozenset(
        part
        for part in subsystem
        if any(connection not in subsystem for connection in outgoing[part])
    )
    for subsystem in subsystems
}

type Signal = str
type FFState = bool
type ConState = dict[ModName, Signal]
type SystemState = dict[ModName, FFState | ConState]


def initial_state() -> SystemState:
    state: SystemState = {}
    for name, mod_type in types.items():
        if mod_type == "%":
            state[name] = False
        elif mod_type == "&":
            if name not in state:
                state[name] = {}
            for prev in incoming[name]:
                state[name][prev] = "low"
    return state


def get_substate(system_state: SystemState, subsystem: Subsystem) -> SystemState:
    return {name: state for name, state in system_state.items() if name in subsystem}


# find subsystem cycles
subsystem_cycles: dict[Subsystem, int] = {}
state = initial_state()
subsystem_histories: dict[Subsystem, list[SystemState]] = {
    sub: [] for sub in subsystems
}
for button_press in count():
    for subsystem in subsystems:
        sub_state = get_substate(state, subsystem)
        if sub_state in subsystem_histories[subsystem]:
            if subsystem not in subsystem_cycles:
                if subsystem_histories[subsystem].index(sub_state) != 0:
                    # subsystems always cycle back to the beginning
                    raise NotImplementedError
                subsystem_cycles[subsystem] = button_press
        else:
            subsystem_histories[subsystem].append(deepcopy(sub_state))

    if all(subsystem in subsystem_cycles for subsystem in subsystems):
        break

    signals = [("button", "low", "broadcaster")]
    while signals:
        source, signal, name = signals.pop(0)
        if name == "rx" and signal == "low":
            running = False
            break
        mod_type = types[name]
        if mod_type == "broadcaster":
            for out in outgoing[name]:
                signals.append((name, signal, out))
        elif mod_type == "%" and signal == "low":
            assert isinstance(state[name], bool)
            state[name] ^= True
            new_signal = "high" if state[name] else "low"
            for out in outgoing[name]:
                signals.append((name, new_signal, out))
        elif mod_type == "&":
            assert isinstance(state[name], dict)
            state[name][source] = signal
            new_signal = (
                "low" if all(s == "high" for s in state[name].values()) else "high"
            )
            for out in outgoing[name]:
                signals.append((name, new_signal, out))

print(subsystem_cycles)
