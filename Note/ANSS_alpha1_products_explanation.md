# Alpha_1 Products Explanation

Product data are generated in `Note/ANSS_alpha1_products.csv` by `Note/generate_alpha1_products.py`.

Source product table: `data/185_BPAANSS_h0.txt`.
Degree and basis source: `data/185_BPAANSS_table.txt`.

The file `185_BPAANSS_h0.txt` has lines of the form `x -> y`, where `h0` denotes multiplication by `alpha_1`. Thus each line records `alpha_1 * x = y` in the ANSS `E_2` page.

For each source generator `x`, the script finds its chart position `(s_1,f_1)` from `185_BPAANSS_table.txt`: the stem `s_1` is the first coordinate in `deg=(s,r)`, and the ANSS filtration `f_1` is the first number in the bracketed generator name `[f-b]`.

Since `alpha_1` has chart degree `(3,1)`, the product lies in `(s_2,f_2)=(s_1+3,f_1+1)`. The generator checks every nonzero target term in the `h0` table and confirms that it has this same position.

Only nonzero products are written to the CSV. Rows are sorted by increasing `s_1`, then increasing `f_1`; if multiple source generators have the same `(s_1,f_1)`, their rows are ordered by source-generator name.

The `product` column is a coordinate vector for `alpha_1*x` in the target group at `(s_2,f_2)=(s_1+3,f_1+1)`. The ordered target basis is the original basis order from `185_BPAANSS_table.txt`, restricted to that target group. Coefficients are reduced mod 3.

Product vectors use square brackets in the CSV so spreadsheet apps do not interpret vectors like `(1)` as accounting notation for `-1`.
