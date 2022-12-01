from pathlib import Path

here = Path(__file__).parent

raw_input = (here / "input.txt").read_text()


def max_three_elf_calories(raw_input: str) -> list[int]:
    elf_calories = [
        sum(int(line) for line in elf_data_raw.splitlines())
        for elf_data_raw in raw_input.split("\n\n")
    ]
    max_three = sorted(elf_calories)[-3:]
    return max_three


print(sum(max_three_elf_calories(raw_input)))
