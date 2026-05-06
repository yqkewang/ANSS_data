#!/usr/bin/env python3
"""Generate ANSS E2 rank tables from the BPAANSS table."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_TABLE = REPO_ROOT / "data" / "185_BPAANSS_table.txt"
MARKDOWN_OUT = REPO_ROOT / "Note" / "ANSS_E2_ranks.md"
CSV_OUT = REPO_ROOT / "Note" / "ANSS_E2_ranks.csv"

EXPLANATION = [
    "Source: `data/185_BPAANSS_table.txt`.",
    "This file lists algebraic Novikov spectral sequence classes. Lines containing `<-` are differential lines of the form `target <- source | dr`, so they are skipped because they do not represent surviving ANSS `E_2` basis generators.",
    "Each remaining line has a generator name and a degree `deg=(s,r)`. The first coordinate `s` is the stem. The second coordinate `r` is Adams filtration, not the ANSS filtration used in this table.",
    "The ANSS filtration `f` is read from the first number in the bracketed generator name `[f-b]`; the second bracket number `b` is a basis/copy index inside that filtration.",
    "Therefore `rank(s,f)` is the number of non-differential generator lines whose degree has stem `s` and whose bracketed generator name begins with `[f-...]`.",
]


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


def write_markdown(rows: list[tuple[int, int, int]], markdown_out: Path) -> None:
    lines = [
        "# ANSS E2 Ranks",
        "",
        "## How This Table Was Generated",
        "",
        *EXPLANATION,
        "",
        "Example: all generators `[0-0]`, `v0^1[0-0]`, ..., `v0^39[0-0]` have stem `s=0` and bracket-first-index `f=0`, so they contribute rank `40` at `(s,f)=(0,0)`.",
        "",
        "## Rank Table",
        "",
        "| s | f | rank |",
        "|---:|---:|---:|",
    ]
    lines.extend(f"| {s} | {f} | {rank} |" for s, f, rank in rows)
    markdown_out.write_text("\n".join(lines) + "\n")


def markdown_table_to_csv(markdown_in: Path, csv_out: Path) -> None:
    rows: list[list[str]] = []
    for line in markdown_in.read_text().splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells == ["s", "f", "rank"]:
            rows.append(cells)
        elif len(cells) == 3 and all(cell.lstrip("-").isdigit() for cell in cells):
            rows.append(cells)

    with csv_out.open("w", newline="") as fh:
        fh.write("# ANSS E2 Ranks\n")
        for explanation_line in EXPLANATION:
            fh.write(f"# {explanation_line.replace('`', '')}\n")
        fh.write("# Data rows begin after the s,f,rank header.\n")
        writer = csv.writer(fh)
        writer.writerows(rows)


def main() -> None:
    rows = parse_ranks(SOURCE_TABLE)
    write_markdown(rows, MARKDOWN_OUT)
    markdown_table_to_csv(MARKDOWN_OUT, CSV_OUT)
    print(f"Wrote {len(rows)} rank rows to {MARKDOWN_OUT.relative_to(REPO_ROOT)}")
    print(f"Wrote CSV export to {CSV_OUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
