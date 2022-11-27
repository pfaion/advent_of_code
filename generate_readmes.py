#!/usr/bin/env python
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


years = sorted(item for item in here.glob("20*") if item.is_dir())
for year in years:

    days = sorted(item for item in year.glob("day*") if item.is_dir())
    for day in days:

        print(f"Generating readme for {day.relative_to(here)}...")
        content = [f"# Day {int(day.name[3:])}"]

        for part in (1, 2):

            html_file = day / f"part{part}.html"
            if not html_file.exists():
                continue
            html = html_file.read_text()
            content += [
                "## Part 1",
                "<details><summary>Exercise Text (click to expand)</summary>",
                html,
                "</details>",
            ]

            variants = sorted(day.glob("part1*.py"))
            for i, variant in enumerate(variants):
                code = variant.read_text()
                result, duration = run_timed(variant)
                content += [
                    f"### Variant {i + 1}",
                    "```python",
                    code,
                    "```",
                    f"Runtime: {round(duration, 3)}s, Output:",
                    "```",
                    result,
                    "```",
                ]

        readme = day / "README.md"
        readme.write_text("\n\n".join(content))
