#!/usr/bin/env python3
"""Generate markdown and CSV tables for beta-family products."""

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
OUTPUTS = [
    {
        "method": "beta2",
        "label": "beta_2",
        "title": "Beta_2 Products",
        "theta": "data/185_BPBocSS_theta3.txt",
        "shift": (26, 2),
        "stem": "beta2",
    },
    {
        "method": "beta33",
        "label": "beta_{3/3}",
        "title": "Beta_{3/3} Products",
        "theta": "data/185_BPBocSS_theta4.txt",
        "shift": (34, 2),
        "stem": "beta33",
    },
    {
        "method": "beta4",
        "label": "beta_4",
        "title": "Beta_4 Products",
        "theta": "data/185_BPBocSS_theta5.txt",
        "shift": (58, 2),
        "stem": "beta4",
    },
    {
        "method": "beta5",
        "label": "beta_5",
        "title": "Beta_5 Products",
        "theta": "data/185_BPBocSS_theta6.txt",
        "shift": (74, 2),
        "stem": "beta5",
    },
    {
        "method": "beta63",
        "label": "beta_{6/3}",
        "title": "Beta_{6/3} Products",
        "theta": "data/185_BPBocSS_theta7.txt",
        "shift": (82, 2),
        "stem": "beta63",
    },
]


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


def markdown_table_to_csv(markdown_in: Path, csv_out: Path, config: dict[str, object]) -> None:
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
        fh.write(f"# {config['title']} in the ANSS E2 Page\n")
        fh.write(f"# Product data are computed by beta.py: ANSSData().{config['method']}(x).\n")
        fh.write(f"# {config['method']} uses B2A_inv, {config['theta']}, and delta to compute products through E_2(S/3).\n")
        fh.write("# Degree and basis source: data/185_BPAANSS_table.txt.\n")
        fh.write("# Only nonzero computable products are displayed.\n")
        fh.write("# Rows are sorted by increasing s_1, then increasing f_1.\n")
        fh.write("# The product column is the coordinate vector in the original target-basis order from 185_BPAANSS_table.txt.\n")
        fh.write("# Product vectors use square brackets in this CSV so spreadsheet apps do not interpret (1) as -1.\n")
        fh.write("# Data rows begin after the s_1,f_1,product header.\n")
        writer = csv.writer(fh)
        writer.writerows(rows)

    print(f"Wrote {csv_out.relative_to(REPO_ROOT)}")


def write_product_files(
    data: ANSSData,
    name_to_degree: dict[str, tuple[int, int]],
    basis_by_degree: dict[tuple[int, int], list[str]],
    config: dict[str, object],
) -> None:
    method_name = str(config["method"])
    label = str(config["label"])
    title = str(config["title"])
    theta = str(config["theta"])
    shift_s, shift_f = config["shift"]
    stem = str(config["stem"])
    markdown_out = REPO_ROOT / "Note" / f"ANSS_{stem}_products.md"
    csv_out = REPO_ROOT / "Note" / f"ANSS_{stem}_products.csv"
    method = getattr(data, method_name)
    product_rows = []
    error_rows = []
    zero_count = 0

    lines = [
        f"# {title} in the ANSS E2 Page",
        "",
        "## How This Table Was Generated",
        "",
        f"Product computation: `ANSSData().{method_name}(x)` in `beta.py`.",
        "Degree and basis source: `data/185_BPAANSS_table.txt`.",
        "",
        f"The method `{method_name}(x)` computes `{label}*x` by the same beta-family composite used for `beta_1`: it applies `B2A_inv`, then the corresponding Moore-spectrum theta multiplication table `{theta}`, then the boundary map `delta` back to sphere names.",
        "",
        "For each source generator `x`, I find its chart position `(s_1,f_1)` from `185_BPAANSS_table.txt`: the stem `s_1` is the first coordinate in `deg=(s,r)`, and the ANSS filtration `f_1` is the first number in the bracketed generator name `[f-b]`.",
        "",
        f"The class `{label}` has chart degree `({shift_s},{shift_f})`, so the product lies in `(s_2,f_2)=(s_1+{shift_s},f_1+{shift_f})`. I checked every nonzero target term returned by `{method_name}` and confirmed that it has this same position.",
        "",
        "Only nonzero computable products are displayed. Rows are sorted by increasing `s_1`, then increasing `f_1`; if multiple source generators have the same `(s_1,f_1)`, their rows are ordered by source-generator name.",
        "",
        f"The `product` column is a coordinate vector for `{label}*x` in the target group at `(s_2,f_2)=(s_1+{shift_s},f_1+{shift_f})`. The ordered target basis is the original basis order from `185_BPAANSS_table.txt`, restricted to that target group. Coefficients are reduced mod 3.",
    ]

    for source in name_to_degree:
        s1, f1 = name_to_degree[source]
        s2, f2 = s1 + shift_s, f1 + shift_f
        try:
            product = method(source)
        except Exception as exc:  # Record edge-of-range table failures without stopping all outputs.
            error_rows.append((source, s1, f1, type(exc).__name__, str(exc)))
            continue

        if product.iszero():
            zero_count += 1
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

    lines.extend(
        [
            "",
            f"Computed summary: `{len(product_rows)}` nonzero rows, `{zero_count}` zero products omitted, `{len(error_rows)}` products skipped because the existing data/code could not compute them.",
        ]
    )

    if error_rows:
        lines.extend(
            [
                "",
                "Skipped computations:",
                "",
                "| source | s_1 | f_1 | error | detail |",
                "|---|---:|---:|---|---|",
            ]
        )
        for source, s1, f1, error_type, detail in error_rows:
            escaped_detail = detail.replace("|", "\\|")
            lines.append(f"| `{source}` | {s1} | {f1} | `{error_type}` | `{escaped_detail}` |")

    lines.extend(
        [
            "",
            "## Product Table",
            "",
            "| s_1 | f_1 | product |",
            "|---:|---:|---|",
        ]
    )

    product_rows.sort(key=lambda row: (row[0], row[1], row[2]))
    lines.extend(row[-1] for row in product_rows)

    markdown_out.write_text("\n".join(lines) + "\n")
    print(f"Wrote {markdown_out.relative_to(REPO_ROOT)} with {len(product_rows)} nonzero products")
    markdown_table_to_csv(markdown_out, csv_out, config)


def main() -> None:
    data = ANSSData()
    name_to_degree, basis_by_degree = parse_degree_data()
    for config in OUTPUTS:
        write_product_files(data, name_to_degree, basis_by_degree, config)


if __name__ == "__main__":
    main()
