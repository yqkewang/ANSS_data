# Beta_{6/3} Products in the ANSS E2 Page

## How This Table Was Generated

Product computation: `ANSSData().beta63(x)` in `beta.py`.
Degree and basis source: `data/185_BPAANSS_table.txt`.

The method `beta63(x)` computes `beta_{6/3}*x` by the same beta-family composite used for `beta_1`: it applies `B2A_inv`, then the corresponding Moore-spectrum theta multiplication table `data/185_BPBocSS_theta7.txt`, then the boundary map `delta` back to sphere names.

For each source generator `x`, I find its chart position `(s_1,f_1)` from `185_BPAANSS_table.txt`: the stem `s_1` is the first coordinate in `deg=(s,r)`, and the ANSS filtration `f_1` is the first number in the bracketed generator name `[f-b]`.

The class `beta_{6/3}` has chart degree `(82,2)`, so the product lies in `(s_2,f_2)=(s_1+82,f_1+2)`. I checked every nonzero target term returned by `beta63` and confirmed that it has this same position.

Only nonzero computable products are displayed. Rows are sorted by increasing `s_1`, then increasing `f_1`; if multiple source generators have the same `(s_1,f_1)`, their rows are ordered by source-generator name.

The `product` column is a coordinate vector for `beta_{6/3}*x` in the target group at `(s_2,f_2)=(s_1+82,f_1+2)`. The ordered target basis is the original basis order from `185_BPAANSS_table.txt`, restricted to that target group. Coefficients are reduced mod 3.

Computed summary: `73` nonzero rows, `503` zero products omitted, `1` products skipped because the existing data/code could not compute them.

Skipped computations:

| source | s_1 | f_1 | error | detail |
|---|---:|---:|---|---|
| `v0^1[1-1]` | 11 | 1 | `KeyError` | `'v0^1v1^1v3^1[3-3]'` |

## Product Table

| s_1 | f_1 | product |
|---:|---:|---|
| 0 | 0 | `(2)` |
| 3 | 1 | `(1)` |
| 10 | 2 | `(0, 1)` |
| 13 | 3 | `(1)` |
| 20 | 4 | `(0, 1)` |
| 23 | 5 | `(1)` |
| 26 | 2 | `(2)` |
| 30 | 6 | `(0, 1)` |
| 33 | 7 | `(1)` |
| 34 | 2 | `(0, 2, 2)` |
| 36 | 4 | `(2)` |
| 37 | 3 | `(0, 2)` |
| 40 | 8 | `(0, 1)` |
| 43 | 9 | `(1)` |
| 44 | 4 | `(0, 2)` |
| 46 | 6 | `(2)` |
| 47 | 5 | `(2)` |
| 50 | 10 | `(0, 1)` |
| 53 | 11 | `(1)` |
| 54 | 6 | `(2)` |
| 56 | 8 | `(2)` |
| 57 | 3 | `(2)` |
| 57 | 7 | `(2)` |
| 58 | 2 | `(0, 1)` |
| 60 | 4 | `(1)` |
| 60 | 12 | `(0, 1)` |
| 61 | 3 | `(0, 1)` |
| 63 | 13 | `(1)` |
| 64 | 8 | `(2)` |
| 66 | 10 | `(2)` |
| 67 | 5 | `(0, 2)` |
| 67 | 9 | `(2)` |
| 68 | 4 | `(2)` |
| 68 | 4 | `(1)` |
| 70 | 6 | `(1)` |
| 70 | 14 | `(0, 1)` |
| 71 | 5 | `(0, 0, 1)` |
| 73 | 15 | `(1)` |
| 74 | 2 | `(2)` |
| 74 | 10 | `(2)` |
| 75 | 5 | `(2)` |
| 76 | 12 | `(2)` |
| 77 | 7 | `(2)` |
| 77 | 11 | `(2)` |
| 78 | 6 | `(2)` |
| 78 | 6 | `(1)` |
| 80 | 8 | `(1)` |
| 80 | 16 | `(0, 1)` |
| 81 | 3 | `(0, 1, 1)` |
| 81 | 3 | `(0, 1, 1)` |
| 81 | 7 | `(0, 1)` |
| 82 | 2 | `(1, 1)` |
| 83 | 17 | `(1)` |
| 84 | 4 | `(1)` |
| 84 | 4 | `(2)` |
| 84 | 12 | `(2)` |
| 85 | 3 | `(0, 2)` |
| 85 | 7 | `(2)` |
| 86 | 14 | `(2)` |
| 87 | 9 | `(2)` |
| 87 | 13 | `(2)` |
| 88 | 8 | `(2)` |
| 88 | 8 | `(1)` |
| 89 | 3 | `(1)` |
| 90 | 10 | `(1)` |
| 91 | 5 | `(0, 1, 1)` |
| 91 | 5 | `(0, 1, 1)` |
| 91 | 9 | `(0, 1)` |
| 92 | 4 | `(0, 2)` |
| 94 | 6 | `(0, 1)` |
| 94 | 6 | `(0, 2)` |
| 95 | 5 | `(0, 2)` |
| 96 | 4 | `(1)` |
