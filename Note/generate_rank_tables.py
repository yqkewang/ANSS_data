#!/usr/bin/env python3
"""Generate a data-only ANSS E2 rank CSV from the BPAANSS table."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_TABLE = REPO_ROOT / "data" / "185_BPAANSS_table.txt"
CSV_OUT = REPO_ROOT / "Note" / "ANSS_E2_ranks.csv"


def parse_ranks(source_table: Path) -> list[tuple[int, int, int]]:
    """Count nonzero ranks by (stem, ANSS filtration)."""
    ranks: Counter[tuple[int, int]] = Counter()

    with source_table.open() as fh:
        for line in fh:
            if "<-" in line:
                continue

            name = line.split("\t", 1)[0]
            deg_match = re.search(r"deg=\((\d+),(\d+)\)", line)
            filt_match = re.search(r"\[(\d+)-\d+\]", name)
            if deg_match is None or filt_match is None:
                raise ValueError(f"Could not parse table line: {line.rstrip()}")

            stem = int(deg_match.group(1))
            filtration = int(filt_match.group(1))
            ranks[(stem, filtration)] += 1

    return [(s, f, rank) for (s, f), rank in sorted(ranks.items())]


def write_csv(rows: list[tuple[int, int, int]], csv_out: Path) -> None:
    with csv_out.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["s", "f", "rank"])
        writer.writerows(rows)


def main() -> None:
    rows = parse_ranks(SOURCE_TABLE)
    write_csv(rows, CSV_OUT)
    print(f"Wrote {len(rows)} rank rows to {CSV_OUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
