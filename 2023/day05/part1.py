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
