# ANSS E2 Ranks Explanation

Rank data are generated in `Note/ANSS_E2_ranks.csv` by `Note/generate_rank_tables.py`.

Source: `data/185_BPAANSS_table.txt`.

This file lists algebraic Novikov spectral sequence classes. Lines containing `<-` are differential lines of the form `target <- source | dr`, so they are skipped because they do not represent surviving ANSS `E_2` basis generators.

Each remaining line has a generator name and a degree `deg=(s,r)`. The first coordinate `s` is the stem. The second coordinate `r` is Adams filtration, not the ANSS filtration used in this table.

The ANSS filtration `f` is read from the first number in the bracketed generator name `[f-b]`; the second bracket number `b` is a basis/copy index inside that filtration.

Therefore `rank(s,f)` is the number of non-differential generator lines whose degree has stem `s` and whose bracketed generator name begins with `[f-...]`.

Example: all generators `[0-0]`, `v0^1[0-0]`, ..., `v0^39[0-0]` have stem `s=0` and bracket-first-index `f=0`, so they contribute rank `40` at `(s,f)=(0,0)`.
