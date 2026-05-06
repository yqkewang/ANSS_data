# Beta_5 Products in the ANSS E2 Page

## How This Table Was Generated

Product computation: `ANSSData().beta5(x)` in `beta.py`.
Degree and basis source: `data/185_BPAANSS_table.txt`.

The method `beta5(x)` computes `beta_5*x` by the same beta-family composite used for `beta_1`: it applies `B2A_inv`, then the corresponding Moore-spectrum theta multiplication table `data/185_BPBocSS_theta6.txt`, then the boundary map `delta` back to sphere names.

For each source generator `x`, I find its chart position `(s_1,f_1)` from `185_BPAANSS_table.txt`: the stem `s_1` is the first coordinate in `deg=(s,r)`, and the ANSS filtration `f_1` is the first number in the bracketed generator name `[f-b]`.

The class `beta_5` has chart degree `(74,2)`, so the product lies in `(s_2,f_2)=(s_1+74,f_1+2)`. I checked every nonzero target term returned by `beta5` and confirmed that it has this same position.

Only nonzero computable products are displayed. Rows are sorted by increasing `s_1`, then increasing `f_1`; if multiple source generators have the same `(s_1,f_1)`, their rows are ordered by source-generator name.

The `product` column is a coordinate vector for `beta_5*x` in the target group at `(s_2,f_2)=(s_1+74,f_1+2)`. The ordered target basis is the original basis order from `185_BPAANSS_table.txt`, restricted to that target group. Coefficients are reduced mod 3.

Computed summary: `47` nonzero rows, `530` zero products omitted, `0` products skipped because the existing data/code could not compute them.

## Product Table

| s_1 | f_1 | product |
|---:|---:|---|
| 0 | 0 | `(2)` |
| 10 | 2 | `(0, 2)` |
| 20 | 4 | `(0, 2)` |
| 26 | 2 | `(2)` |
| 30 | 6 | `(0, 2)` |
| 34 | 2 | `(1)` |
| 36 | 4 | `(2)` |
| 40 | 8 | `(0, 2)` |
| 44 | 4 | `(1)` |
| 46 | 6 | `(2)` |
| 50 | 10 | `(0, 2)` |
| 54 | 6 | `(1)` |
| 56 | 8 | `(2)` |
| 57 | 3 | `(2)` |
| 58 | 2 | `(2)` |
| 60 | 12 | `(0, 2)` |
| 64 | 8 | `(1)` |
| 66 | 10 | `(2)` |
| 67 | 5 | `(2)` |
| 68 | 4 | `(1)` |
| 68 | 4 | `(2)` |
| 70 | 14 | `(0, 2)` |
| 74 | 2 | `(2)` |
| 74 | 10 | `(1)` |
| 76 | 12 | `(2)` |
| 77 | 7 | `(2)` |
| 78 | 6 | `(1)` |
| 78 | 6 | `(2)` |
| 80 | 16 | `(0, 2)` |
| 82 | 2 | `(2)` |
| 84 | 12 | `(1)` |
| 86 | 14 | `(2)` |
| 87 | 9 | `(2)` |
| 88 | 8 | `(1)` |
| 88 | 8 | `(2)` |
| 89 | 3 | `(0, 2, 1)` |
| 90 | 18 | `(0, 2)` |
| 92 | 4 | `(1)` |
| 94 | 14 | `(1)` |
| 96 | 4 | `(0, 1, 2)` |
| 97 | 11 | `(2)` |
| 98 | 10 | `(1)` |
| 98 | 10 | `(2)` |
| 102 | 6 | `(0, 1)` |
| 105 | 3 | `(2)` |
| 106 | 2 | `(0, 2)` |
| 106 | 2 | `(0, 2)` |
