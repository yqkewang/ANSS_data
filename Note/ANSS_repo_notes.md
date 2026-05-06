# Notes on the ANSS Data Repository

Date explored: 2026-05-05

## Executive Summary

This repository does not itself recompute the algebraic Novikov spectral sequence from first principles. The heavy computation was done externally by the modified `MinimalResolution` program described in `README.md`; this repo stores the resulting tables in `data/`, a chart PDF, and a small Python interface for reading the tables and asking for degrees and products.

The main Python entry point is `beta.py`. Its class `ANSSData` parses the table files and exposes methods such as `in_deg`, `three`, `alpha1`, `beta1`, `beta2`, `beta33`, `beta4`, `beta5`, and `beta63`.

For the two points you asked about:

1. The code does not store a precomputed "rank list" as a separate object or file. The generator list for the ANSS `E_2` page is built in `ANSSData.make_deg_table` from `data/185_BPAANSS_table.txt`, skipping algebraic Novikov differential lines. Ranks are obtained by counting generators in `data.deg_table` with the same `(stem, ANSS filtration)`. The helper `data.in_deg(stem, filtration)` returns the generators in one bidegree, so the rank is `len(data.in_deg(stem, filtration))`.
2. Products by `3` and `alpha_1` are direct table lookups from `data/185_BPAANSS_a0.txt` and `data/185_BPAANSS_h0.txt`. Products by beta classes are computed on demand by composing: translate sphere generators to Moore-space/Bockstein names, multiply by a theta table on `E_2(S/3)`, then apply the boundary map `delta` back to sphere names.

## Repository Layout

| Path | Purpose |
| --- | --- |
| `README.md` | Mathematical overview, source of the data, table conventions, and examples for using `beta.py`. |
| `anss_E2_158.pdf` | Chart of the `E_2` page through the displayed range. The README explains the visual key. |
| `beta.py` | Main parser/query API. Loads data tables and implements degree lookup and products. |
| `lincomb.py` | Small finite-field linear-combination class used by `beta.py`. |
| `data/*.txt` | Precomputed algebraic Novikov, Bockstein, translation, and multiplication tables. |
| `Note/ANSS_repo_notes.md` | This note. |

The data files were generated outside this repository by running the modified `MinimalResolution` tools listed in the README:

```text
./mr_st 185 90
./BPtab 185
./mr_BP 185 40
```

The file prefix `185` means the data are computed through Adams-Novikov internal degree 185, not necessarily through stem 185. In this parsed data, the largest stem represented among permanent-cycle sphere generators is 182.

## Runtime Setup

`beta.py` imports `frozendict` through `lincomb.py`. That package was missing, so I installed it into a local virtual environment:

```bash
python3 -m venv .venv
.venv/bin/pip install frozendict
```

I also added `.venv/` to `.gitignore`.

Pandoc was already available at `/opt/homebrew/bin/pandoc`, so no markdown compiler dependency was needed. This note can be compiled to HTML with:

```bash
pandoc Note/ANSS_repo_notes.md -o Note/ANSS_repo_notes.html
```

## Data File Formats

### Sphere algebraic Novikov table

`data/185_BPAANSS_table.txt` describes the algebraic Novikov spectral sequence converging to the sphere ANSS `E_2` page.

Permanent-cycle lines look like:

```text
[0-0]	|deg=(0,0)
```

Differential lines look like:

```text
v0^1[2-0]	<-	[1-1]	|d2	|deg=(10,3)
```

For the code in this repository, only the permanent-cycle lines are used to build the ANSS `E_2` generator degree table. Differential lines are skipped by `make_deg_table`.

Counts observed:

| File | Permanent lines | Differential lines |
| --- | ---: | ---: |
| `185_BPAANSS_table.txt` | 577 | 1155 |
| `185_BPBocSS_table.txt` | 513 | 12049 |

Most Bockstein differential lines are `d0` lines; `beta.py` ignores `d0` entries when building the boundary information.

### Multiplication and translation tables

Multiplication and translation files use:

```text
source	->	target1+target2+o
```

Here `o` means the zero/noise term and is ignored by `parse_mult`. Repeated terms cancel or combine mod 3 because targets are stored as `LinComb` objects over `F_3`.

Important files:

| File | Meaning in the code |
| --- | --- |
| `185_BPAANSS_a0.txt` | Sphere multiplication by `3`, exposed as `data.three(...)`. |
| `185_BPAANSS_h0.txt` | Sphere multiplication by `alpha_1`, exposed as `data.alpha1(...)`. |
| `185_BPBocSS_a0.txt` | Moore/Bockstein multiplication by `3`, used when translating boundary values. |
| `185_BPBocSS_h0.txt` | Moore/Bockstein multiplication by `alpha_1`; parsed but not exposed by a public method. |
| `185_BPB2A_table.txt` | Translation from Bockstein/Moore names to algebraic Novikov sphere names. |
| `185_BPBocSS_theta2.txt` | Moore-space multiplication used to compute `beta1`. |
| `185_BPBocSS_theta3.txt` | Moore-space multiplication used to compute `beta2`. |
| `185_BPBocSS_theta4.txt` | Moore-space multiplication used to compute `beta33`, i.e. `beta_{3/3}`. |
| `185_BPBocSS_theta5.txt` | Moore-space multiplication used to compute `beta4`. |
| `185_BPBocSS_theta6.txt` | Moore-space multiplication used to compute `beta5`. |
| `185_BPBocSS_theta7.txt` | Moore-space multiplication used to compute `beta63`, i.e. `beta_{6/3}`. |

Line counts:

| File | Lines |
| --- | ---: |
| `185_BPAANSS_table.txt` | 1732 |
| `185_BPAANSS_a0.txt` | 567 |
| `185_BPAANSS_h0.txt` | 564 |
| `185_BPB2A_table.txt` | 513 |
| `185_BPBocSS_table.txt` | 12562 |
| `185_BPBocSS_a0.txt` | 605 |
| `185_BPBocSS_h0.txt` | 12562 |
| each `185_BPBocSS_theta*.txt` | 391904 |

The theta tables are huge and sparse: almost all lines map to `o`, but they are still parsed into memory by `ANSSData.__init__`.

## `lincomb.py`

`lincomb.py` defines `LinComb`, a linear combination of named generators over `F_3`.

Key behavior:

| Method | Meaning |
| --- | --- |
| `__init__` | Drops coefficients that are zero mod 3. |
| `__repr__` | Prints `0`, `x`, `2x`, or sums such as `x + 2y`. |
| `add`, `add_inplace` | Addition mod 3. |
| `scalar` | Scalar multiplication mod 3. |
| `map` | Applies a function from generator names to `LinComb` objects linearly. This is what lets products extend from generators to sums. |

Small code notes:

- `lincomb.py` requires the external package `frozendict`.
- `LinComb.deserialize` calls `re.split` but `lincomb.py` does not import `re`. That method is not used by the current repository workflow.
- The constructor uses a mutable default argument `elts={}`. In this particular implementation the default object is filtered into a fresh dict before assignment, but the pattern is still worth knowing about.

## `beta.py`: Object Construction

The central class is `ANSSData`.

When you run:

```python
from beta import *
data = ANSSData()
```

the constructor loads the whole data set:

1. `beta_mapping` maps theta files to public beta operation names.
2. `make_bockstein()` parses `185_BPBocSS_table.txt` into:
   - `self.bockstein`: string-to-string dictionary for nonzero Bockstein differentials and permanent cycles.
   - `self.bottom_cells`: permanent-cycle Bockstein classes.
3. `parse_mult()` loads all multiplication/translation files into `dict[str, LinComb]`.
4. `make_deg_table()` builds `self.deg_table`, the degree table for sphere ANSS `E_2` generators.
5. `make_B2A()` loads Bockstein-to-algebraic-Novikov name conversion.
6. `make_B2A_inv()` builds a partial inverse that models the quotient map `q: E_2(S) -> E_2(S/3)`.
7. `make_boc_a0div()` inverts Bockstein multiplication by 3 where possible, for use inside `delta`.

Parsed object sizes from this repo:

| Object | Size |
| --- | ---: |
| `data.deg_table` | 577 generators |
| `data.a0table` | 567 entries |
| `data.h0table` | 564 entries |
| `data.bockstein` | 1025 entries |
| `data.bottom_cells` | 513 entries |
| nonzero Bockstein entries | 512 entries |
| `data.B2A` | 513 entries |
| `data.B2A_inv` | 577 entries |
| `data.boc_a0div` | 591 entries |
| each `data.beta_table[...]` | 391904 entries |

## Where Ranks Come From

The relevant code is `ANSSData.make_deg_table()` in `beta.py`.

Its input is:

```text
data/185_BPAANSS_table.txt
```

Its rule is:

1. Read every line.
2. If the line contains `<-`, skip it because it is an algebraic Novikov differential.
3. Parse `deg=(stem, Adams filtration)`.
4. Extract the ANSS filtration from the generator name. For a name like `[3-0]`, the ANSS filtration is `3`; for `v0^2[3-0]`, it is still `3`.
5. Store:

```python
self.deg_table[name] = {
    "s": stem,
    "f": anss_filt,
    "nov": adams_filt - anss_filt,
}
```

So `deg_table` is the true generator list used by the code for the sphere ANSS `E_2` page.

The helper:

```python
data.in_deg(stem, filtration)
```

returns all generator names in a fixed `(stem, ANSS filtration)`. Therefore:

```python
rank = len(data.in_deg(stem, filtration))
```

This is the rank/dimension over `F_3` represented by the parsed basis in that bidegree.

To generate a complete rank list:

```python
from collections import Counter
from beta import ANSSData

data = ANSSData()
rank_by_degree = Counter(
    (row["s"], row["f"])
    for row in data.deg_table.values()
)

for (stem, filtration), rank in sorted(rank_by_degree.items()):
    print(stem, filtration, rank)
```

Observed rank summary:

| Quantity | Value |
| --- | ---: |
| Sphere `E_2` generators in `deg_table` | 577 |
| Occupied `(stem, ANSS filtration)` bidegrees | 424 |
| Maximum rank in one bidegree | 40 |
| Highest represented stem | 182 |
| Highest represented ANSS filtration | 31 |

Sample degree lookups:

```python
data.in_deg(3, 1)
# ['[1-0]']

len(data.in_deg(3, 1))
# 1

data.show_deg("[1-0]")
# (3, 1, 0)
```

The rank at `(0, 0)` is 40 because the file contains the 3-divisibility tower:

```python
data.in_deg(0, 0)[:8]
# ['[0-0]', 'v0^1[0-0]', 'v0^2[0-0]', 'v0^3[0-0]',
#  'v0^4[0-0]', 'v0^5[0-0]', 'v0^6[0-0]', 'v0^7[0-0]']
```

## Where Product Lists Come From

The "product information" in this repository means multiplication of each listed `E_2` generator by a small set of important named elements. It is not a general two-input multiplication function that accepts arbitrary classes `x` and `y`.

The available sphere `E_2` multiplication operations are:

| Operation in Python | Mathematical product |
| --- | --- |
| `data.three(x)` | `3x`, equivalently multiplication by `v0`/`a0` in the tables |
| `data.alpha1(x)` | `alpha_1 x`, called `h0` in the table filenames |
| `data.beta1(x)` | `beta_1 x` |
| `data.beta2(x)` | `beta_2 x` |
| `data.beta33(x)` | `beta_{3/3} x` |
| `data.beta4(x)` | `beta_4 x` |
| `data.beta5(x)` | `beta_5 x` |
| `data.beta63(x)` | `beta_{6/3} x` |

Each operation is a linear map on the `F_3`-basis of generators. For example, once the code knows `alpha_1 x` and `alpha_1 y`, it computes `alpha_1(x + 2y)` by linearity:

```text
alpha_1(x + 2y) = alpha_1 x + 2 alpha_1 y
```

A product-table line has the form:

```text
source	->	target1+target2+o
```

This means "the chosen multiplier times `source` is the linear combination of target terms." The symbol `o` is ignored by `parse_mult`; it represents zero/no extra term in this Python interface. Repeated target names are added in `F_3`, so two copies of the same term print with coefficient `2`, and three copies cancel.

For example, in `185_BPAANSS_a0.txt`:

```text
[0-0]	->	v0^1[0-0]+o
```

means:

```text
3 * [0-0] = v0^1[0-0]
```

and in `185_BPAANSS_h0.txt`:

```text
[0-0]	->	[1-0]+o
```

means:

```text
alpha_1 * [0-0] = [1-0]
```

There is no single final file containing every sphere `E_2` product. Products are either direct table lookups or are computed from several tables.

### Multiplication by `3`

Loaded in `ANSSData.__init__` as:

```python
self.a0table = self.parse_mult(self.file_prefix + "_BPAANSS_a0.txt")
```

Public method:

```python
data.three(x)
```

For a generator string, this returns `self.a0table[x]`. For a `LinComb`, it maps linearly over the terms.

The source data file is `data/185_BPAANSS_a0.txt`. Its entries are already in algebraic Novikov/sphere notation, so no name translation is needed. The file gives the product on generators; `LinComb.map` extends it to sums.

### Multiplication by `alpha_1`

Loaded in `ANSSData.__init__` as:

```python
self.h0table = self.parse_mult(self.file_prefix + "_BPAANSS_h0.txt")
```

Public method:

```python
data.alpha1(x)
```

Again, strings are looked up directly and linear combinations are handled term-by-term.

The source data file is `data/185_BPAANSS_h0.txt`. As with multiplication by `3`, this table is already a sphere `E_2` table in algebraic Novikov notation.

### Beta products

Beta products are more complicated because the raw data files do not directly say:

```text
beta_i * sphere_generator -> sphere_linear_combination
```

Instead, the computation uses the mod-3 Moore spectrum `S/3`. The theta files describe multiplication on `E_2(S/3)` by classes whose boundary images are beta elements in `E_2(S)`. Therefore `beta.py` has to translate into Moore/Bockstein names, multiply there, and translate back.

The beta methods are:

```python
data.beta1(x)
data.beta2(x)
data.beta33(x)
data.beta4(x)
data.beta5(x)
data.beta63(x)
```

They all call:

```python
data.beta_n(n, x)
```

For a generator `x`, `beta_n` performs:

```python
rtn = self.B2A_inv[x]
rtn = rtn.map(lambda s: self.beta_table["beta" + n][s])
rtn = rtn.map(lambda s: self.delta(s))
```

Mathematically, this is:

1. Apply `q: E_2(S) -> E_2(S/3)` using `B2A_inv`.
2. Multiply on `E_2(S/3)` by the theta class corresponding to the desired beta element.
3. Apply the boundary map `delta: E_2(S/3) -> E_2(S)`.

So a beta product is not a direct lookup in one final beta table. It is the composite:

```text
E_2(S) --q--> E_2(S/3) --theta_i--> E_2(S/3) --delta--> E_2(S)
```

The code names for these pieces are:

| Piece | Code object | Data source |
| --- | --- | --- |
| `q` from sphere to Moore names | `self.B2A_inv` | inverse of `185_BPB2A_table.txt`, with divisible/edge cases removed |
| theta multiplication on Moore classes | `self.beta_table[...]` | one of the `185_BPBocSS_theta*.txt` files |
| boundary back to sphere classes | `self.delta(...)` | `185_BPBocSS_table.txt`, `185_BPBocSS_a0.txt`, and `185_BPB2A_table.txt` |

The theta-to-beta mapping is:

| Method | Theta table |
| --- | --- |
| `beta1` | `185_BPBocSS_theta2.txt` |
| `beta2` | `185_BPBocSS_theta3.txt` |
| `beta33` | `185_BPBocSS_theta4.txt` |
| `beta4` | `185_BPBocSS_theta5.txt` |
| `beta5` | `185_BPBocSS_theta6.txt` |
| `beta63` | `185_BPBocSS_theta7.txt` |

### The boundary map `delta`

`delta` is the most subtle part of `beta.py`.

Input: a Bockstein/Moore generator name.

Process:

1. Look up the Bockstein differential in `self.bockstein`.
2. Permanent cycles map to zero.
3. If the Bockstein target is divisible by 3 in Bockstein notation, repeatedly divide using `self.boc_a0div`.
4. Convert the resulting non-3-divisible Bockstein names to algebraic Novikov names using `self.B2A`.
5. Re-apply the required powers of 3 using `self.boc_a0table`.

This implements the README's statement that a Bockstein differential `d_r(x)=y` gives `delta(x)=y/3`, with extra work needed because generator names are leading-term names and not literal monomials.

### Generating a complete product list

To list products in the sphere ANSS `E_2` page, iterate through `data.deg_table`.

```python
from beta import ANSSData

data = ANSSData()
ops = ["three", "alpha1", "beta1", "beta2", "beta33", "beta4", "beta5", "beta63"]

for g in sorted(data.deg_table):
    for op in ops:
        try:
            value = getattr(data, op)(g)
        except KeyError as err:
            value = f"missing table entry: {err}"
        print(g, op, value)
```

Some products near the edge of the computation raise `KeyError` because the multiplication table does not contain the needed target/source beyond the computed range. I observed:

| Operation | Nonzero results | Zero results | Key errors |
| --- | ---: | ---: | ---: |
| `three` | 63 | 504 | 10 |
| `alpha1` | 237 | 327 | 13 |
| `beta1` | 368 | 209 | 0 |
| `beta2` | 200 | 377 | 0 |
| `beta33` | 211 | 366 | 0 |
| `beta4` | 137 | 440 | 0 |
| `beta5` | 47 | 530 | 0 |
| `beta63` | 73 | 503 | 1 |

Examples matching the README and parser run:

```python
data.alpha1("[1-0]")
# 0

data.three("[1-0]")
# 0

data.beta1("[1-0]")
# 2[3-0]

data.beta2("[2-2]")
# 2[4-4]

data.alpha1(data.beta2("[2-2]"))
# 2[5-4]
```

## Important Code Quirks

### Duplicate `make_B2A`

`beta.py` defines `make_B2A` twice. The first definition manually parses `185_BPB2A_table.txt`; the second definition, later in the class, simply calls `parse_mult`.

In Python, the second definition wins. So the active method is:

```python
def make_B2A(self):
    return self.parse_mult(self.file_prefix + "_BPB2A_table.txt")
```

The earlier definition is dead code.

### Unused specialized `make_boc_a0table`

There is a method `make_boc_a0table` that filters Bockstein multiplication-by-3 targets to remove terms killed by `d0`s. However, `__init__` currently sets:

```python
self.boc_a0table = self.parse_mult(self.file_prefix + "_BPBocSS_a0.txt")
```

so the specialized method is not used. The inversion step in `make_boc_a0div` does have an exclusion function for `d0`-related terms, but the raw `boc_a0table` object itself is the unfiltered parse.

### Python warnings

Running under Python 3.14 emits `SyntaxWarning`s for regex strings like `"\+"`, `"\|"`, and `"\["`. The code still runs, but these should eventually be raw strings such as `r"\+"`.

### No command-line interface

The repository is meant to be used from an interactive Python interpreter or a small ad hoc script. There is no CLI, package metadata, or test suite.

## Practical Recipes

Start Python with the local environment:

```bash
.venv/bin/python
```

Load the data:

```python
from beta import *
data = ANSSData()
```

Find generators in a bidegree:

```python
data.in_deg(3, 1)
```

Get one generator's degree:

```python
data.show_deg("[1-0]")
```

Compute products:

```python
data.three("[0-0]")
data.alpha1("[0-0]")
data.beta1("[1-0]")
data.beta2("[2-2]")
```

Generate rank data:

```python
from collections import Counter

ranks = Counter((r["s"], r["f"]) for r in data.deg_table.values())
```

Generate all nonzero beta1 products:

```python
for g in sorted(data.deg_table):
    y = data.beta1(g)
    if y:
        print(f"{g} -> {y}")
```

## Verification Performed

I verified the following locally:

1. Created `.venv` and installed `frozendict`.
2. Imported `beta.py` successfully with `.venv/bin/python`.
3. Instantiated `ANSSData()`, which parsed all data files.
4. Checked README examples:
   - `data.in_deg(3, 1)` returns `['[1-0]']`.
   - `data.beta1("[1-0]")` returns `2[3-0]`.
   - `data.alpha1("[1-0]")` returns `0`.
   - `data.alpha1(data.beta2("[2-2]"))` returns `2[5-4]`.
5. Confirmed Pandoc is available for compiling this markdown note.
