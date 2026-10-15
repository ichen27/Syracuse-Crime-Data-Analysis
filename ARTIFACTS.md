# Artifact index

Version: analysis package 0.2.0; snapshot identified by SHA-256 in the audit.

| Artifact | Purpose and use |
|---|---|
| [crime_data.db](crime_data.db) | Existing SQLite source snapshot; input to `syracuse-analyze`. Open in SQLite or Python. |
| [findings.md](reports/findings.md) | Readable findings, exclusions, annual totals, and interpretation limits. |
| [summary.json](reports/summary.json) | Aggregate counts, calendar denominators, per-table audit, and source hash. |
| [overview.png](reports/overview.png) | Finished chart panel, viewable without Python. |
| [src/syracuse_crime](src/syracuse_crime/) | Editable loader and figure/report generation source. |
| [analysis.ipynb](legacy/analysis.ipynb) | Original notebook, retained as historical context; not current validated results. |
| [original scripts and report](legacy/) | Preserved original exploration; outside the supported quickstart. |

Reproduce the maintained outputs with the README quickstart. Reports contain aggregates, not addresses or individual records. Environments, caches, and scratch runs are intentionally excluded. The existing source database is retained; no new raw records are published by this update.
