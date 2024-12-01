from pathlib import Path

rules = [
    line.split()
    for line in Path(__file__).with_name("input.txt").read_text().splitlines()
]

state = {}
while rules:
    rule = rules.pop(0)
    match rule:
        case source, "->", target:
            if source.isdigit():
                state[target] = int(source)
            else:
                if source not in state:
                    rules.append(rule)
                    continue
                state[target] = state[source]
        case "NOT", source, "->", target:
            if source not in state:
                rules.append(rule)
                continue
            state[target] = (1 << 16) - 1 - state[source]
        case op1, "AND", op2, "->", target:
            if op1.isdigit():
                if op2 not in state:
                    rules.append(rule)
                    continue
                state[target] = int(op1) & state[op2]
            else:
                if op1 not in state or op2 not in state:
                    rules.append(rule)
                    continue
                state[target] = state[op1] & state[op2]
        case op1, "OR", op2, "->", target:
            if op1 not in state or op2 not in state:
                rules.append(rule)
                continue
            state[target] = state[op1] | state[op2]
        case op1, "LSHIFT", op2, "->", target:
            if op1 not in state:
                rules.append(rule)
                continue
            state[target] = state[op1] << int(op2)
        case op1, "RSHIFT", op2, "->", target:
            if op1 not in state:
                rules.append(rule)
                continue
            state[target] = state[op1] >> int(op2)

print(state["a"])
