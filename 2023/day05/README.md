# Day 5

[Exercise Text](https://adventofcode.com/2023/day/5)

## Part 1
```python
import re
from dataclasses import dataclass
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text()

seeds_raw, data_raw = data_raw.split("\n\n", maxsplit=1)
seeds = [int(val) for val in seeds_raw.split(": ")[1].split()]


@dataclass
class MappingSection:
    start: int
    stop: int
    offset: int


@dataclass
class CategoryValue:
    category: str
    value: int


@dataclass
class Mapping:
    source: str
    destination: str
    sections: list[MappingSection]

    def map(self, value: CategoryValue) -> CategoryValue:
        if value.category != self.source:
            raise ValueError(f"Tried mapping {value} with {self}")
        for section in self.sections:
            if section.start <= value.value <= section.stop:
                return CategoryValue(
                    category=self.destination, value=value.value + section.offset
                )
        return CategoryValue(category=self.destination, value=value.value)


source_mappings: dict[str, Mapping] = {}

for mapping_raw in data_raw.split("\n\n"):
    mapping_lines = mapping_raw.splitlines()
    match = re.match(r"(?P<source>\w+)-to-(?P<destination>\w+) map:", mapping_lines[0])
    source, destination = match.groups()
    mapping = Mapping(source=source, destination=destination, sections=[])
    for line in mapping_lines[1:]:
        destination_start, source_start, length = map(int, line.split())
        mapping.sections.append(
            MappingSection(
                start=source_start,
                stop=source_start + length - 1,
                offset=destination_start - source_start,
            )
        )
    source_mappings[source] = mapping


def calculate_seed_location(seed: int) -> int:
    value = CategoryValue(category="seed", value=seed)
    while value.category != "location":
        mapping = source_mappings[value.category]
        value = mapping.map(value)
    return value.value


print(min(calculate_seed_location(seed) for seed in seeds))

```
Runtime: 0.048s, Size: 2001, Output:
```
993500720
```
## Part 2
```python
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from rich import print

data_raw = Path(__file__).with_name("input.txt").read_text()

seeds_raw, data_raw = data_raw.split("\n\n", maxsplit=1)
seeds_raw_values = list(map(int, seeds_raw.split(": ")[1].split()))
seed_ranges_raw = list(zip(seeds_raw_values[::2], seeds_raw_values[1::2]))


@dataclass
class CategoryRange:
    category: str
    start: int
    stop: int


seed_ranges = [
    CategoryRange(category="seed", start=start, stop=start + length - 1)
    for start, length in seed_ranges_raw
]


@dataclass
class MappingSection:
    start: int
    stop: int
    offset: int


@dataclass
class Mapping:
    source: str
    destination: str
    sections: list[MappingSection]

    def map(self, cat_range: CategoryRange) -> Iterator[CategoryRange]:
        if cat_range.category != self.source:
            raise ValueError(f"Tried mapping {cat_range} with {self}")
        matched_anything = False
        for section in self.sections:
            overlap_start = max(section.start, cat_range.start)
            overlap_stop = min(section.stop, cat_range.stop)
            if overlap_start <= overlap_stop:
                yield CategoryRange(
                    category=self.destination,
                    start=overlap_start + section.offset,
                    stop=overlap_stop + section.offset,
                )
                matched_anything = True
            else:
                continue
            if cat_range.start < overlap_start:
                yield from self.map(
                    CategoryRange(
                        category=cat_range.category,
                        start=cat_range.start,
                        stop=overlap_start - 1,
                    )
                )
            if cat_range.stop > overlap_stop:
                yield from self.map(
                    CategoryRange(
                        category=cat_range.category,
                        start=overlap_stop + 1,
                        stop=cat_range.stop,
                    )
                )
        if not matched_anything:
            yield CategoryRange(
                category=self.destination,
                start=cat_range.start,
                stop=cat_range.stop,
            )


source_mappings: dict[str, Mapping] = {}

for mapping_raw in data_raw.split("\n\n"):
    mapping_lines = mapping_raw.splitlines()
    match = re.match(r"(?P<source>\w+)-to-(?P<destination>\w+) map:", mapping_lines[0])
    source, destination = match.groups()
    mapping = Mapping(source=source, destination=destination, sections=[])
    for line in mapping_lines[1:]:
        destination_start, source_start, length = map(int, line.split())
        mapping.sections.append(
            MappingSection(
                start=source_start,
                stop=source_start + length - 1,
                offset=destination_start - source_start,
            )
        )
    source_mappings[source] = mapping


def calculate_min_location(seed_range: CategoryRange) -> int:
    current_ranges = [seed_range]
    while current_ranges[0].category != "location":
        mapping = source_mappings[current_ranges[0].category]
        current_ranges = [
            new_range
            for cat_range in current_ranges
            for new_range in mapping.map(cat_range)
        ]
    starts = [r.start for r in current_ranges]
    return min(starts)


print(min(calculate_min_location(seed_range) for seed_range in seed_ranges))

```
Runtime: 0.273s, Size: 3545, Output:
```
4917124
```