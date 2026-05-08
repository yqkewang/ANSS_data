#!/usr/bin/env python3
"""Generate a data-only CSV table for multiplication by 3."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEGREE_TABLE = REPO_ROOT / "data" / "185_BPAANSS_table.txt"
MULTIP3_TABLE = REPO_ROOT / "data" / "185_BPAANSS_a0.txt"
CSV_OUT = REPO_ROOT / "Note" / "ANSS_multip3.csv"


def parse_degree_data() -> tuple[
    dict[str, tuple[int, int]],
    dict[tuple[int, int], list[str]],
    dict[str, int],
]:
    """Return generator degrees, basis lists by (stem, ANSS filtration), and basis order."""
    name_to_degree: dict[str, tuple[int, int]] = {}
    basis_by_degree: dict[tuple[int, int], list[str]] = defaultdict(list)
    name_to_index: dict[str, int] = {}

    with DEGREE_TABLE.open() as fh:
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
            name_to_degree[name] = (stem, filtration)
            basis_by_degree[(stem, filtration)].append(name)
            name_to_index[name] = len(name_to_index)

    return name_to_degree, basis_by_degree, name_to_index


def parse_linear_combination(raw_target: str) -> dict[str, int]:
    """Parse a + separated target expression as an F_3 linear combination."""
    terms: dict[str, int] = {}
    for term in raw_target.split("+"):
        if term == "o":
            continue
        terms[term] = (terms.get(term, 0) + 1) % 3
        if terms[term] == 0:
            del terms[term]
    return terms


def vector_for_terms(terms: dict[str, int], target_basis: list[str]) -> tuple[int, ...]:
    """Return coordinates in the target basis order from BPAANSS_table."""
    return tuple(terms.get(term, 0) for term in target_basis)


def format_csv_vector(vector: tuple[int, ...]) -> str:
    return f"[{', '.join(str(entry) for entry in vector)}]"


def write_csv() -> None:
    name_to_degree, basis_by_degree, name_to_index = parse_degree_data()
    product_rows = []
    source_names = set()
    nonzero_count = 0

    with MULTIP3_TABLE.open() as fh:
        for line in fh:
            source, raw_target = line.rstrip("\n").split("\t->\t")
            source_names.add(source)
            if source not in name_to_degree:
                raise ValueError(f"Source {source} is not in {DEGREE_TABLE.relative_to(REPO_ROOT)}")

            stem, filtration = name_to_degree[source]
            terms = parse_linear_combination(raw_target)
            for target in terms:
                if target not in name_to_degree:
                    raise ValueError(f"Target {target} is not in {DEGREE_TABLE.relative_to(REPO_ROOT)}")
                target_degree = name_to_degree[target]
                if target_degree != (stem, filtration):
                    raise ValueError(
                        f"{source} target {target} has degree {target_degree}, expected {(stem, filtration)}"
                    )

            basis = basis_by_degree[(stem, filtration)]
            vector = vector_for_terms(terms, basis)
            if any(vector):
                nonzero_count += 1
            product_rows.append(
                (
                    stem,
                    filtration,
                    name_to_index[source],
                    format_csv_vector(vector),
                )
            )

    product_rows.sort(key=lambda row: (row[0], row[1], row[2]))
    missing_sources = set(name_to_degree) - source_names

    with CSV_OUT.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["s", "f", "product"])
        for stem, filtration, _source_index, product in product_rows:
            writer.writerow([stem, filtration, product])

    print(
        f"Wrote {CSV_OUT.relative_to(REPO_ROOT)} with {len(product_rows)} products, "
        f"{nonzero_count} nonzero products, and {len(missing_sources)} basis generators absent from the a0 table"
    )


if __name__ == "__main__":
    write_csv()
