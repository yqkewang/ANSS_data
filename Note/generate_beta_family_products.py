#!/usr/bin/env python3
"""Generate data-only CSV tables and one explanation file for beta-family products."""

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
EXPLANATION_OUT = REPO_ROOT / "Note" / "ANSS_beta_family_products_explanation.md"
OUTPUTS = [
    {
        "method": "beta1",
        "label": "beta_1",
        "title": "Beta_1 Products",
        "theta": "data/185_BPBocSS_theta2.txt",
        "shift": (10, 2),
        "stem": "beta1",
    },
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


def format_csv_vector(vector: tuple[int, ...]) -> str:
    """Format vectors with brackets so spreadsheet apps keep entries nonnegative."""
    return f"[{', '.join(str(entry) for entry in vector)}]"


def write_product_csv(
    data: ANSSData,
    name_to_degree: dict[str, tuple[int, int]],
    basis_by_degree: dict[tuple[int, int], list[str]],
    config: dict[str, object],
) -> dict[str, object]:
    method_name = str(config["method"])
    shift_s, shift_f = config["shift"]
    stem = str(config["stem"])
    csv_out = REPO_ROOT / "Note" / f"ANSS_{stem}_products.csv"
    method = getattr(data, method_name)
    product_rows = []
    error_rows = []
    zero_count = 0

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
                format_csv_vector(vector),
            )
        )

    product_rows.sort(key=lambda row: (row[0], row[1], row[2]))

    with csv_out.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["s_1", "f_1", "product"])
        for s1, f1, _source, product in product_rows:
            writer.writerow([s1, f1, product])

    print(
        f"Wrote {csv_out.relative_to(REPO_ROOT)} with {len(product_rows)} nonzero products, "
        f"{zero_count} zero products omitted, and {len(error_rows)} skipped computations"
    )
    return {
        "config": config,
        "csv_out": csv_out,
        "nonzero_count": len(product_rows),
        "zero_count": zero_count,
        "error_rows": error_rows,
    }


def write_combined_explanation(summaries: list[dict[str, object]]) -> None:
    lines = [
        "# Beta-Family Products Explanation",
        "",
        "Product CSV files are generated by `Note/generate_beta_family_products.py`.",
        "",
        "Degree and basis source: `data/185_BPAANSS_table.txt`.",
        "",
        "Each beta-family method computes products by the same beta-family composite used for `beta_1`: it applies `B2A_inv`, then the corresponding Moore-spectrum theta multiplication table, then the boundary map `delta` back to sphere names.",
        "",
        "For each source generator `x`, the script finds its chart position `(s_1,f_1)` from `185_BPAANSS_table.txt`: the stem `s_1` is the first coordinate in `deg=(s,r)`, and the ANSS filtration `f_1` is the first number in the bracketed generator name `[f-b]`.",
        "",
        "If a class has chart degree `(a,b)`, then its product with `x` lies in `(s_2,f_2)=(s_1+a,f_1+b)`. The generator checks every nonzero target term returned by the product method and confirms that it has this same position.",
        "",
        "Only nonzero computable products are written to the CSV files. Rows are sorted by increasing `s_1`, then increasing `f_1`; if multiple source generators have the same `(s_1,f_1)`, their rows are ordered by source-generator name.",
        "",
        "The `product` column is a coordinate vector in the target group. The ordered target basis is the original basis order from `185_BPAANSS_table.txt`, restricted to that target group. Coefficients are reduced mod 3.",
        "",
        "Product vectors use square brackets in the CSV files so spreadsheet apps do not interpret vectors like `(1)` as accounting notation for `-1`.",
        "",
        "## Product Files",
        "",
        "| class | CSV | method | theta table | chart degree | nonzero rows | zero products omitted | skipped computations |",
        "|---|---|---|---|---:|---:|---:|---:|",
    ]

    for summary in summaries:
        config = summary["config"]
        csv_out = summary["csv_out"]
        shift_s, shift_f = config["shift"]
        error_rows = summary["error_rows"]
        lines.append(
            f"| `{config['label']}` | `{csv_out.relative_to(REPO_ROOT)}` | "
            f"`ANSSData().{config['method']}(x)` | `{config['theta']}` | "
            f"`({shift_s},{shift_f})` | {summary['nonzero_count']} | "
            f"{summary['zero_count']} | {len(error_rows)} |"
        )

    skipped = [
        (summary["config"], error_row)
        for summary in summaries
        for error_row in summary["error_rows"]
    ]
    if skipped:
        lines.extend(
            [
                "",
                "## Skipped Computations",
                "",
                "These are skipped because the existing data/code could not compute them.",
                "",
                "| class | source | s_1 | f_1 | error | detail |",
                "|---|---|---:|---:|---|---|",
            ]
        )
        for config, (source, s1, f1, error_type, detail) in skipped:
            escaped_detail = detail.replace("|", "\\|")
            lines.append(
                f"| `{config['label']}` | `{source}` | {s1} | {f1} | "
                f"`{error_type}` | `{escaped_detail}` |"
            )

    EXPLANATION_OUT.write_text("\n".join(lines) + "\n")
    print(f"Wrote {EXPLANATION_OUT.relative_to(REPO_ROOT)}")


def main() -> None:
    data = ANSSData()
    name_to_degree, basis_by_degree = parse_degree_data()
    summaries = []
    for config in OUTPUTS:
        summaries.append(write_product_csv(data, name_to_degree, basis_by_degree, config))
    write_combined_explanation(summaries)


if __name__ == "__main__":
    main()
