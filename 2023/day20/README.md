# Day 20

[Exercise Text](https://adventofcode.com/2023/day/20)

## Part 1
```python
import re
from collections import defaultdict
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

# parse data
outgoing = defaultdict(list)
incoming = defaultdict(list)
types = defaultdict(lambda: None, **{"broadcaster": "broadcaster"})
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

# setup module states
ff_states: dict[str, bool] = {}
con_states: dict[str, dict[str, str]] = defaultdict(dict)
for name, mod_type in types.items():
    if mod_type == "%":
        ff_states[name] = False
    elif mod_type == "&":
        for prev in incoming[name]:
            con_states[name][prev] = "low"

# run
counts = {"low": 0, "high": 0}
for _ in range(1000):
    signals = [("button", "low", "broadcaster")]
    counts["low"] += 1
    while signals:
        source, signal, name = signals.pop(0)
        mod_type = types[name]
        if mod_type == "broadcaster":
            for out in outgoing[name]:
                signals.append((name, signal, out))
                counts[signal] += 1
        elif mod_type == "%" and signal == "low":
            ff_states[name] ^= True
            new_signal = "high" if ff_states[name] else "low"
            for out in outgoing[name]:
                signals.append((name, new_signal, out))
                counts[new_signal] += 1
        elif mod_type == "&":
            con_states[name][source] = signal
            new_signal = (
                "low" if all(s == "high" for s in con_states[name].values()) else "high"
            )
            for out in outgoing[name]:
                signals.append((name, new_signal, out))
                counts[new_signal] += 1

print(counts["low"] * counts["high"])

```
Runtime: 0.063s, Size: 1997, Output:
```
1020211150
```
## Part 2
```python
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

```
Runtime: 0.13s, Size: 3339, Output:
```
238815727638557
```