# Multiplication by 3 Explanation

Product data are generated in `Note/ANSS_multip3.csv` by `Note/generate_multip3.py`.

Source product table: `data/185_BPAANSS_a0.txt`.
Degree and basis source: `data/185_BPAANSS_table.txt`.

The file `185_BPAANSS_a0.txt` has lines of the form `x -> y`, where `a0` records multiplication by 3. Thus each line records `3*x = y` in the ANSS `E_2` page.

For each source generator `x`, the script finds its chart position `(s,f)` from `185_BPAANSS_table.txt`: the stem `s` is the first coordinate in `deg=(s,r)`, and the ANSS filtration `f` is the first number in the bracketed generator name `[f-b]`.

Multiplication by 3 has chart degree `(0,0)`, so `3*x` lies in the same chart position `(s,f)` as `x`. The generator checks every nonzero target term in the `a0` table and confirms that it has this same position.

The `product` column is a coordinate vector for `3*x` in the group at `(s,f)`. The ordered target basis is the original basis order from `185_BPAANSS_table.txt`, restricted to that group. Coefficients are reduced mod 3.

Rows are sorted by increasing `s`, then increasing `f`. When several source generators have the same `(s,f)`, their rows follow the original source-basis order from `185_BPAANSS_table.txt`; this matters because the CSV does not include a separate source-generator column.

Zero products are included. For example, a zero product in a rank-two group is written as `[0, 0]`.

The `a0` table contains 567 source rows. Ten permanent-cycle basis generators from `185_BPAANSS_table.txt` do not appear as sources in `185_BPAANSS_a0.txt`, so the CSV contains rows only for the source generators whose multiplication by 3 is present in the `a0` table.
