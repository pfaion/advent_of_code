#!/usr/bin/env python
import argparse
import re
import subprocess
import time
from pathlib import Path

here = Path(__file__).parent


def run_timed(path: Path) -> tuple[str, float]:
    t0 = time.perf_counter()
    result = subprocess.check_output(
        f"/usr/bin/env python {path}", shell=True, encoding="utf-8"
    ).strip()
    t1 = time.perf_counter()
    return result, (t1 - t0)


parser = argparse.ArgumentParser()
parser.add_argument("year", nargs="?")
parser.add_argument("day", nargs="?")
args = parser.parse_args()

years = sorted(item for item in here.glob("20*") if item.is_dir())
if args.year is not None:
    if not any(args.year == year.name for year in years):
        raise ValueError(f"A folder for year '{args.year}' does not exist!")
    years = [year for year in years if year.name == args.year]
for year in years:

    days = sorted(item for item in year.glob("day*") if item.is_dir())
    if args.day is not None:
        if not any(int(args.day) == int(day.name[3:]) for day in days):
            raise ValueError(f"A folder for day '{args.day}' does not exist!")
        days = [day for day in days if int(day.name[3:]) == int(args.day)]
    for day in days:

        print(f"Generating readme for {day.relative_to(here)}...")

        content = [
            f"# Day {int(day.name[3:])}",
            "",
            f"[Exercise Text](https://adventofcode.com/{year.name}/day/{int(day.name[3:])})",
            "",
        ]

        for part in (1, 2):
            part_data = {}
            content += [f"## Part {part}"]

            variants_data = []
            source_files = sorted(day.glob(f"part{part}*.py"))
            for i, path in enumerate(source_files):
                code = path.read_text()
                result, runtime = run_timed(path)
                variants_data.append((i, code, runtime, result))

            if len(variants_data) > 1:
                content += [
                    "### Overview",
                    "| Variant | Runtime | Size |",
                    "| --- | --- | --- |",
                ]
                for i, code, runtime, result in variants_data:
                    content += [f"|{i+1}|{round(runtime, 3)}s|{len(code)}|"]
                content += [""]

            for i, code, runtime, result in variants_data:
                if len(variants_data) > 1:
                    content += [f"### Variant {i + 1}"]
                content += [
                    "```python",
                    code,
                    "```",
                    f"Runtime: {round(runtime, 3)}s, Size: {len(code)}, Output:",
                    "```",
                    result,
                    "```",
                ]

        readme = day / "README.md"
        readme.write_text("\n".join(content))
