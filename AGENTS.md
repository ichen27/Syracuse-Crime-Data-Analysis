# Syracuse analysis maintenance

Repository: `ichen27/Syracuse-Crime-Data-Analysis`. Read README.md for setup and validation commands; ARTIFACTS.md indexes deliverables.

- `src/syracuse_crime/data.py` owns the shared schema/date contract used by the companion model repository. Changes need regression tests for both supported category-column names and source date formats.
- Open source databases read-only. Preserve the existing snapshot. Save aggregate reports and figures in `reports/`; use ignored `work/` for scratch outputs.
- Maintain source-record terminology, coverage caveats, and explicit calendar denominators. Keep partial years separate from full-year comparisons.
- `legacy/` preserves original work and is outside the maintained execution path.
- Run lint, tests, and report generation before pushing a feature branch. Review the diff, create a PR, and wait for current-revision CI before merging within authorized scope. Keep the companion dependency pinned to an inspected commit.
