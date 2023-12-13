import re
from dataclasses import dataclass
from functools import cache
from itertools import takewhile
from pathlib import Path

# from rich import print


data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

conditions, groups_raw = zip(*(line.split() for line in data_raw))
all_groups = [tuple(line.split(",")) for line in groups_raw]


@cache
def get_pattern(groups: tuple[str]) -> re.Pattern:
    return re.compile(
        r"^[\.\?]*"
        + r"[\.\?]+".join(r"[#\?]{" + n + r"}" for n in groups)
        + r"[\.\?]*$"
    )


@dataclass(frozen=True)
class State:
    condition: str = ""
    groups: tuple[str] = tuple()


@cache
def lstrip(state: State) -> State:
    condition = str(state.condition)
    groups = list(state.groups)
    while True:
        if condition.startswith("."):
            condition = condition.lstrip(".")
            continue
        if not condition.startswith("#"):
            break
        if not groups:
            break
        leading_hash = len(list(takewhile("#".count, condition)))
        leading_hashable = len(list(takewhile("#?".count, condition)))
        if leading_hash <= (first_group := int(groups[0])) <= leading_hashable:
            # need to cut off one more, to ensure that group will be separated from next
            condition = condition[first_group + 1 :]
            groups.pop(0)
            continue
        break
    return State(condition, tuple(groups))


assert lstrip(State("")) == State()
assert lstrip(State("...")) == State()
assert lstrip(State("...#")) == State("#")
assert lstrip(State("#...", (1,))) == State()
assert lstrip(State("..#.#..", (1, 1, 1))) == State("", (1,))
assert lstrip(State("?")) == State("?")
assert lstrip(State("..?#..", (2,))) == State("?#..", (2,))
assert lstrip(State("..##??..", (1,))) == State("##??..", (1,))
assert lstrip(State("..##??..", (2,))) == State("?..")
assert lstrip(State("..##??..", (3,))) == State()
assert lstrip(State("..##??..", (4,))) == State()
assert lstrip(State("#?#?#??", (1, 1, 1))) == State("?")
assert lstrip(State("###", (1, 1, 3))) == State("###", (1, 1, 3))


def validate_filled(state: State) -> bool:
    assert "?" not in state.condition
    actual_groups = re.findall(r"#", state.condition)
    if len(actual_groups) != len(state.groups):
        return False
    return all(
        len(actual_group) == int(group)
        for actual_group, group in zip(actual_groups, state.groups)
    )


assert not validate_filled(State("###", (1, 1, 3)))


@cache
def possible_assignments(state: State) -> int:
    if state.groups and not state.condition:
        # print(state, 0)
        return 0

    if not state.groups:
        r = int("#" not in state.condition)
        # print(state, r)
        return r

    if "?" not in state.condition:
        r = int(validate_filled(state))
        # print(state, r)
        return r

    result = 0
    # print(state, "...")
    for branch in [state.condition.replace("?", v, 1) for v in (".", "#")]:
        stripped = lstrip(State(branch, state.groups))
        # print("...", branch, "->", stripped)
        result += possible_assignments(stripped)
    # print(state, result)
    return result


assert possible_assignments(State("##.", ("1", "1", "3"))) == 0


repeat = 5
result = 0
for i, (condition, groups) in enumerate(zip(conditions, all_groups)):
    condition = "?".join(condition for _ in range(repeat))
    groups = groups * repeat
    line_result = possible_assignments(State(condition, groups))
    result += line_result
    print(i, line_result)

print(result)
