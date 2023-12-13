import re
from dataclasses import dataclass
from pathlib import Path

from rich import print

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

conditions, groups_raw = zip(*(line.split() for line in data_raw))
all_groups = [[int(v) for v in line.split(",")] for line in groups_raw]


@dataclass
class State:
    assignment: str
    groups: list[int]
    group_index: int
    last_group_end: int


debug = print
debug = lambda *x: x

repeat = 5
result = 0
for i, (condition, groups) in enumerate(zip(conditions, all_groups)):
    condition = "?".join(condition for _ in range(repeat))
    groups = groups * repeat
    pattern = re.compile(
        r"^[\.\?]*"
        + r"[\.\?]+".join(r"[#\?]{" + str(n) + r"}" for n in groups)
        + r"[\.\?]*$"
    )
    stack = [State(condition, groups, 0, -1)]
    line_result = 0
    while stack:
        state: State = stack.pop()
        debug()
        if not pattern.match(state.assignment):
            debug(f"checking {state}")
            debug("impossible")
            continue
        if state.group_index == len(state.groups):
            print(f"checking {state}")
            debug("finished!")
            line_result += 1
            continue

        # calculate next group earliest start
        n_preceding = sum(size for size in state.groups[: state.group_index])
        min_start = 0
        for char in state.assignment:
            if n_preceding == 0:
                break
            if char == "#":
                n_preceding -= 1
            min_start += 1
        min_start = max(min_start, state.last_group_end + 1)

        # calculate next group latest end
        max_end = len(state.assignment) - sum(
            size for size in state.groups[state.group_index + 1 :]
        )

        # search
        debug(f"trying all in [{min_start}:{max_end}]")
        size = state.groups[state.group_index]
        for offset in range(max_end - min_start - size + 1):
            expanded = f".{state.assignment}."
            start = min_start + offset
            end = min_start + offset + size
            start_e = start + 1
            end_e = end + 1
            debug(f"  trying [{start_e}:{end_e}] in {expanded}")
            if expanded[start_e - 1] == "#":
                debug(f"    impossible: {start_e - 1} == #")
                continue
            if "." in expanded[start_e:end_e]:
                debug(f"    impossible: . in [{start_e}: {end_e}]")
                continue
            if expanded[end_e] == "#":
                debug(f"    impossible: {end_e} == #")
                continue
            # if (
            #     expanded[start] == "#"
            #     or "." in expanded[start_e:end_e]
            #     or expanded[end] == "#"
            # ):
            #     debug("    impossible")
            #     continue
            new_assignment_expanded = (
                expanded[:start] + "." + "#" * size + "." + expanded[end_e + 1 :]
            )
            new_assignment = new_assignment_expanded[1:-1]
            debug(f"    continuing with: {new_assignment}")
            stack.append(
                State(new_assignment, state.groups, state.group_index + 1, end)
            )

    result += line_result
    print(f"{i+1}/{len(all_groups)}: {line_result}")
    break

print(result)
