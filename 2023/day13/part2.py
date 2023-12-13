import copy
from collections.abc import Iterator
from pathlib import Path

from rich import print

data_raw = Path(__file__).with_name("input.txt").read_text()

patterns = data_raw.split("\n\n")

type Lines = list[list[str]]
type Point = tuple[int, int]


def find_reflection_lines(lines: Lines) -> Iterator[int]:
    n_lines = len(lines)
    for i in range(n_lines - 1):
        if all(
            lines[i - offset] == lines[i + offset + 1]
            for offset in range(min(i + 1, n_lines - i - 1))
        ):
            yield i


def stringdiff(a: str, b: str) -> int:
    return sum(ca != cb for ca, cb in zip(a, b))


def smudgepos(a: str, b: str) -> int:
    assert stringdiff(a, b) == 1
    return next(i for i, (ca, cb) in enumerate(zip(a, b)) if ca != cb)


def find_possible_smudges(lines: Lines) -> Iterator[Point]:
    n_lines = len(lines)
    for i in range(n_lines - 1):
        total_diff = 0
        smudges = []
        for offset in range(min(i + 1, n_lines - i - 1)):
            i1 = i - offset
            i2 = i + offset + 1
            a = lines[i1]
            b = lines[i2]
            diff = stringdiff(a, b)
            total_diff += diff
            if diff > 1:
                break
            if diff == 1:
                x = smudgepos(a, b)
                smudges = [(i1, x), (i2, x)]
        if total_diff == 1:
            yield from smudges


def toggle(cell: str) -> str:
    return "#" if cell == "." else "."


def transpose(lines: Lines) -> Lines:
    return [list(col) for col in zip(*lines)]


DEBUG = False


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


result = 0
for i, pattern in enumerate(patterns):
    rows = [list(row) for row in pattern.splitlines()]
    cols = transpose(rows)
    debug(i)
    debug(rows)

    prev_reflections = [
        (kind, reflection)
        for kind, lines in (("r", rows), ("c", cols))
        for reflection in find_reflection_lines(lines)
    ]
    assert len(prev_reflections) == 1
    prev_reflection = prev_reflections[0]
    debug("Has reflection at:", prev_reflection)

    new_reflection = None
    for kind, lines in (("r", rows), ("c", cols)):
        if new_reflection is not None:
            break
        for x, y in find_possible_smudges(lines):
            debug("Evaluating smudge at", x, ",", y)
            lines_copy = copy.deepcopy(lines)
            lines_copy[x][y] = toggle(lines_copy[x][y])
            debug(lines_copy)
            transposed = transpose(lines_copy)
            transposed_kind = ({"r", "c"} - {kind}).pop()
            reflections = {
                (kind, reflection)
                for kind, lines in ((kind, lines_copy), (transposed_kind, transposed))
                for reflection in find_reflection_lines(lines)
            }
            debug("Reflections after toggling smudge:", reflections)
            assert len(reflections) > 0, "Smudges should cause 1 new reflection!"
            new_reflections = reflections - {prev_reflection}
            debug("New reflections:", new_reflections)
            if len(new_reflections) == 0:
                debug("Discarding, would have no new reflections!")
                continue
            if len(new_reflections) > 1:
                debug("Discarding, would have more than 1 new reflections!")
                continue
            new_reflection = new_reflections.pop()
            debug(f"Found smudge: {x},{y} leading to new reflection: {new_reflection}")
            break
    assert new_reflection is not None, "No new reflection found!"

    pattern_result = new_reflection[1] + 1
    if new_reflection[0] == "r":
        pattern_result *= 100
    debug(f"Result for pattern {i}: {pattern_result}")
    result += pattern_result

print(result)
