#!/usr/bin/env python3
"""Generate markdown and CSV tables for beta_1 products."""

from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from beta import ANSSData  # noqa: E402


DEGREE_TABLE = REPO_ROOT / "data" / "185_BPAANSS_table.txt"
MARKDOWN_OUT = REPO_ROOT / "Note" / "ANSS_beta1_products.md"
CSV_OUT = REPO_ROOT / "Note" / "ANSS_beta1_products.csv"


def parse_degree_data() -> tuple[dict[str, tuple[int, int]], dict[tuple[int, int], list[str]]]:
    """Return generator degrees and basis lists by (stem, ANSS filtration)."""
    name_to_degree: dict[str, tuple[int, int]] = {}
    basis_by_degree: dict[tuple[int, int], list[str]] = defaultdict(list)

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

    return name_to_degree, basis_by_degree


def vector_for_terms(terms: dict[str, int], target_basis: list[str]) -> tuple[int, ...]:
    """Return coordinates in the target basis order from BPAANSS_table."""
    return tuple(terms.get(term, 0) for term in target_basis)


def format_markdown_vector(vector: tuple[int, ...]) -> str:
    return f"`({', '.join(str(entry) for entry in vector)})`"


def markdown_table_to_csv(markdown_in: Path, csv_out: Path) -> None:
    rows: list[list[str]] = []
    for line in markdown_in.read_text().splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if cells == ["s_1", "f_1", "product"]:
            rows.append(cells)
        elif len(cells) == 3 and cells[0].isdigit() and cells[1].isdigit():
            if cells[2].startswith("(") and cells[2].endswith(")"):
                cells[2] = f"[{cells[2][1:-1]}]"
            rows.append(cells)

    with csv_out.open("w", newline="") as fh:
        fh.write("# Beta_1 Products in the ANSS E2 Page\n")
        fh.write("# Product data are computed by beta.py: ANSSData().beta1(x).\n")
        fh.write("# beta1 uses B2A_inv, data/185_BPBocSS_theta2.txt, and delta to compute products through E_2(S/3).\n")
        fh.write("# Degree and basis source: data/185_BPAANSS_table.txt.\n")
        fh.write("# Only nonzero products are displayed.\n")
        fh.write("# Rows are sorted by increasing s_1, then increasing f_1.\n")
        fh.write("# The product column is the coordinate vector in the original target-basis order from 185_BPAANSS_table.txt.\n")
        fh.write("# Product vectors use square brackets in this CSV so spreadsheet apps do not interpret (1) as -1.\n")
        fh.write("# Data rows begin after the s_1,f_1,product header.\n")
        writer = csv.writer(fh)
        writer.writerows(rows)

    print(f"Wrote {csv_out.relative_to(REPO_ROOT)}")


def write_markdown() -> None:
    data = ANSSData()
    name_to_degree, basis_by_degree = parse_degree_data()
    product_rows = []

    lines = [
        "# Beta_1 Products in the ANSS E2 Page",
        "",
        "## How This Table Was Generated",
        "",
        "Product computation: `ANSSData().beta1(x)` in `beta.py`.",
        "Degree and basis source: `data/185_BPAANSS_table.txt`.",
        "",
        "Unlike multiplication by `alpha_1`, beta products are not direct lookups in a sphere-product table. The method `beta1(x)` computes the composite `E_2(S) -> E_2(S/3) -> E_2(S/3) -> E_2(S)`: it applies `B2A_inv`, then the theta2 multiplication table `data/185_BPBocSS_theta2.txt`, then the boundary map `delta` back to sphere names.",
        "",
        "For each source generator `x`, I find its chart position `(s_1,f_1)` from `185_BPAANSS_table.txt`: the stem `s_1` is the first coordinate in `deg=(s,r)`, and the ANSS filtration `f_1` is the first number in the bracketed generator name `[f-b]`.",
        "",
        "The class `beta_1` has chart degree `(10,2)`, so the product lies in `(s_2,f_2)=(s_1+10,f_1+2)`. I checked every nonzero target term returned by `beta1` and confirmed that it has this same position.",
        "",
        "Only nonzero products are displayed. Rows are sorted by increasing `s_1`, then increasing `f_1`; if multiple source generators have the same `(s_1,f_1)`, their rows are ordered by source-generator name.",
        "",
        "The `product` column is a coordinate vector for `beta_1*x` in the target group at `(s_2,f_2)=(s_1+10,f_1+2)`. The ordered target basis is the original basis order from `185_BPAANSS_table.txt`, restricted to that target group. Coefficients are reduced mod 3.",
        "",
        "## Product Table",
        "",
        "| s_1 | f_1 | product |",
        "|---:|---:|---|",
    ]

    for source in name_to_degree:
        s1, f1 = name_to_degree[source]
        s2, f2 = s1 + 10, f1 + 2
        product = data.beta1(source)
        if product.iszero():
            continue

        terms = dict(product.elts)
        for target in terms:
            target_degree = name_to_degree[target]
            if target_degree != (s2, f2):
                raise ValueError(
                    f"{source} target {target} has degree {target_degree}, expected {(s2, f2)}"
                )

        basis = basis_by_degree.get((s2, f2), [])
        vector = vector_for_terms(terms, basis)
        product_rows.append(
            (
                s1,
                f1,
                source,
                f"| {s1} | {f1} | {format_markdown_vector(vector)} |",
            )
        )

    product_rows.sort(key=lambda row: (row[0], row[1], row[2]))
    lines.extend(row[-1] for row in product_rows)

    MARKDOWN_OUT.write_text("\n".join(lines) + "\n")
    print(f"Wrote {MARKDOWN_OUT.relative_to(REPO_ROOT)} with {len(product_rows)} nonzero products")


if __name__ == "__main__":
    write_markdown()
    markdown_table_to_csv(MARKDOWN_OUT, CSV_OUT)
