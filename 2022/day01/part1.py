from pathlib import Path

here = Path(__file__).parent

raw_input = (here / "input.txt").read_text()


def max_elf_calories(raw_input: str) -> int:
    elf_calories = [
        sum(int(line) for line in elf_data_raw.splitlines())
        for elf_data_raw in raw_input.split("\n\n")
    ]
    return max(elf_calories)


print(max_elf_calories(raw_input))
