import re
from collections import defaultdict
from math import lcm
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

#######################################################################################
#                   realize subsystems are counters: priceless!                       #
#######################################################################################

# find subsystem inputs
subsystem_inputs = {
    subsystem: frozenset(
        part
        for part in subsystem
        if any(
            part in outputs
            for node, outputs in outgoing.items()
            if node not in subsystem
        )
    )
    for subsystem in subsystems
}

# find counter chains and which connect to the gate
type CounterBit = tuple[ModName, bool]
chains: dict[Subsystem, list[CounterBit]] = {}
assert all(len(inputs) == 1 for inputs in subsystem_inputs.values())
for subsystem in subsystems:
    first = next(iter(subsystem_inputs[subsystem]))
    is_connected = any(types[out] == "&" for out in outgoing[first])
    chains[subsystem] = [(first, is_connected)]
for subsystem, chain in chains.items():
    while True:
        last, _ = chain[-1]
        nexts = [node for node in outgoing[last] if types[node] == "%"]
        if len(nexts) == 0:
            break
        elif len(nexts) == 1:
            node = nexts[0]
            is_connected = any(types[out] == "&" for out in outgoing[node])
            chain.append((node, is_connected))
        else:
            assert False

# calculate when counter is firing
counter_values = {
    subsystem: sum(
        2**bit_i for bit_i, (_, is_connected) in enumerate(chain) if is_connected
    )
    for subsystem, chain in chains.items()
}

print(lcm(*counter_values.values()))
