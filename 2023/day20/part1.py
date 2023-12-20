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
