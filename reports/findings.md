# Historical snapshot findings

Retained **55,779 records** from **55,851** rows in the 2020–2024 source tables; excluded **72** rows. See `summary.json` for per-table reconciliation.

| Source calendar year | Retained records |
|---|---:|
| 2020 | 13,284 |
| 2021 | 12,051 |
| 2022 | 12,335 |
| 2023 | 13,330 |
| 2024 (partial) | 4,779 |

![Overview](overview.png)

## Interpretation

The 31st occurs fewer times than other day numbers. The chart divides each day number's total by its occurrences in 2020–2023; raw totals alone cannot establish an end-of-month decline.

Categories are the source labels after whitespace/case normalization. The 2022 Part 2 column is `CODE DEFINED`, and its US-style dates are explicitly supported.

## Limitations

- 2024 is partial; it is excluded from seasonality comparisons.
- Calendar denominators assume coverage throughout 2020–2023; zero rows do not prove zero incidents.
- Reporting and collection completeness are not independently verified.
- Record counts do not measure individual risk, causality, or crime rates per resident.
- No trustworthy incident-hour or coordinates are available consistently across the snapshot.
