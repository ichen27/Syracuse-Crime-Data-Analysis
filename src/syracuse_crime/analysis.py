"""Generate an aggregate report and portable, noninteractive figures."""

import argparse
import calendar
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from .data import load_records


def calendar_summary(records, start, end, component):
    """Divide record totals by calendar exposure, including zero-record dates."""
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    selected = records.loc[records.date.between(start, end)]
    days = pd.date_range(start, end, freq="D")
    if component not in {"day", "dayofweek", "month"}:
        raise ValueError("Unsupported calendar component")
    exposure = pd.Series(getattr(days, component)).value_counts().sort_index()
    counts = selected.groupby(getattr(selected.date.dt, component)).size()
    return pd.DataFrame({"records": counts.reindex(exposure.index, fill_value=0),
                         "calendar_days": exposure}).assign(
        records_per_day=lambda df: df.records / df.calendar_days
    )


def analyze(database, output):
    records, audit = load_records(database)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    # Fixed historical comparison window; partial 2024 is shown separately.
    start, end = "2020-01-01", "2023-12-31"
    complete = records.loc[records.date.between(start, end)]
    annual = records.groupby(records.date.dt.year).size()
    categories = records.category.value_counts()
    monthly = complete.groupby(complete.date.dt.to_period("M")).size().reindex(
        pd.period_range(start, end, freq="M"), fill_value=0
    )
    summaries = {key: calendar_summary(records, start, end, key)
                 for key in ("month", "dayofweek", "day")}
    report = {
        "audit": audit,
        "annual_record_counts": {str(k): int(v) for k, v in annual.items()},
        "category_counts": {str(k): int(v) for k, v in categories.items()},
        "comparison_window": {"start": start, "end": end},
        "calendar_summaries": {k: v.rename_axis(k).reset_index().to_dict("records")
                               for k, v in summaries.items()},
        "limitations": [
            "2024 is partial; it is excluded from seasonality comparisons.",
            "Calendar denominators assume coverage throughout 2020–2023; zero rows do not prove zero incidents.",
            "Reporting and collection completeness are not independently verified.",
            "Record counts do not measure individual risk, causality, or crime rates per resident.",
            "No trustworthy incident-hour or coordinates are available consistently across the snapshot.",
        ],
    }
    (output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False,
                         "axes.spines.right": False, "figure.dpi": 160})
    fig, axes = plt.subplots(2, 2, figsize=(13, 9), layout="constrained")
    top = categories.head(10).sort_values()
    axes[0, 0].barh(top.index, top.values, color="#146c94")
    axes[0, 0].set(title="Most common record categories · all retained dates", xlabel="Records")
    axes[0, 1].plot(monthly.index.to_timestamp(), monthly.values, color="#146c94")
    axes[0, 1].set(title="Monthly record totals · 2020–2023", ylabel="Records")
    axes[0, 1].xaxis.set_major_locator(mdates.YearLocator())
    axes[0, 1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    dow = summaries["dayofweek"]
    axes[1, 0].bar(list(calendar.day_abbr), dow.records_per_day, color="#146c94")
    axes[1, 0].set(title="Weekday comparison · 2020–2023", ylabel="Records / calendar day")
    dom = summaries["day"]
    axes[1, 1].plot(dom.index, dom.records_per_day, marker=".", color="#146c94")
    axes[1, 1].set(title="Day of month · adjusted for calendar frequency",
                   xlabel="Day of month", ylabel="Records / calendar day")
    fig.suptitle("Syracuse crime records: historical snapshot", fontsize=19, weight="bold")
    fig.savefig(output / "overview.png")
    plt.close(fig)
    lines = ["# Historical snapshot findings", "",
             f"Retained **{len(records):,} records** from **{audit['raw_rows']:,}** rows in the 2020–2024 source tables; "
             f"excluded **{audit['excluded_rows']:,}** rows. See `summary.json` for per-table reconciliation.", "",
             "| Source calendar year | Retained records |", "|---|---:|"]
    lines += [f"| {year}{' (partial)' if year == 2024 else ''} | {count:,} |"
              for year, count in annual.items()]
    lines += ["", "![Overview](overview.png)", "", "## Interpretation", "",
              "The 31st occurs fewer times than other day numbers. The chart divides each day number's "
              "total by its occurrences in 2020–2023; raw totals alone cannot establish an end-of-month decline.", "",
              "Categories are the source labels after whitespace/case normalization. "
              "The 2022 Part 2 column is `CODE DEFINED`, and its US-style dates are explicitly supported.", "",
              "## Limitations", ""] + [f"- {line}" for line in report["limitations"]]
    (output / "findings.md").write_text("\n".join(lines) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=Path("crime_data.db"))
    parser.add_argument("--output", type=Path, default=Path("reports"))
    args = parser.parse_args()
    try:
        report = analyze(args.database, args.output)
    except (ValueError, FileNotFoundError) as exc:
        parser.error(str(exc))
    print(f"Wrote {args.output}: {report['audit']['retained_rows']:,} retained records")


if __name__ == "__main__":
    main()
