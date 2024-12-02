from collections.abc import Iterable, Iterator
from enum import Enum, auto
from pathlib import Path

# read in data
data_raw = Path(__file__).with_name("input.txt").read_text().strip()

# parse data
type Report = list[int]
reports: list[Report] = [list(map(int, line.split())) for line in data_raw.splitlines()]


def pairwise[T](data: Iterable[T]) -> Iterator[tuple[T, T]]:
    for a, b in zip(data[:-1], data[1:]):
        yield a, b


def is_safe(report: Report) -> bool:
    class Mode(Enum):
        NONE = auto()
        INCREASING = auto()
        DECREASING = auto()

    mode = Mode.NONE
    for a, b in pairwise(report):
        if a < b:
            if mode == Mode.DECREASING:
                return False
            mode = Mode.INCREASING
        elif a > b:
            if mode == Mode.INCREASING:
                return False
            mode = Mode.DECREASING
        difference = abs(a - b)
        if not (1 <= difference <= 3):
            return False
    return True


n_safe_reports = 0
for report in reports:
    if is_safe(report):
        n_safe_reports += 1
        continue
    for index_to_remove in range(len(report)):
        modified = report.copy()
        modified.pop(index_to_remove)
        if is_safe(modified):
            n_safe_reports += 1
            break


print(n_safe_reports)
