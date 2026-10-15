import sqlite3

import pandas as pd
import pytest

from syracuse_crime.analysis import calendar_summary
from syracuse_crime.data import load_records, parse_date


@pytest.mark.parametrize('value,expected', [
    ('2020/01/05 05:00:00+00', '2020-01-05'),
    ('2021/01/01 00:00:00+00', '2021-01-01'),
    ('1/2/2022 12:00:00 AM', '2022-01-02'),
    ('02/29/2020', '2020-02-29'),
    ('2024-05-20', '2024-05-20'),
])
def test_date_formats_preserve_calendar_day(value, expected):
    assert parse_date(value) == pd.Timestamp(expected)


@pytest.mark.parametrize('value', [None, '', 'garbage', '02/30/2024'])
def test_invalid_dates(value):
    assert pd.isna(parse_date(value))


def test_spaced_column_and_audit(tmp_path):
    db = tmp_path / 'input.db'
    with sqlite3.connect(db) as conn:
        conn.execute('CREATE TABLE crime_2022_2 (DATEEND TEXT, "CODE DEFINED" TEXT)')
        conn.executemany('INSERT INTO crime_2022_2 VALUES (?, ?)', [
            ('1/2/2022 12:00:00 AM', ' simple assault '),
            ('1/2/2022 12:00:00 AM', ' simple assault '),
            ('bad', 'LARCENY'), ('1/1/2012', 'LARCENY'), ('1/3/2022', None),
        ])
    before = db.read_bytes()
    records, audit = load_records(db)
    assert list(records.category) == ['SIMPLE ASSAULT', 'SIMPLE ASSAULT']
    assert audit['raw_rows'] == 5
    assert audit['retained_rows'] == 2
    assert audit['excluded_rows'] == 3
    assert db.read_bytes() == before


def test_missing_column_fails_instead_of_sqlite_literal(tmp_path):
    db = tmp_path / 'input.db'
    with sqlite3.connect(db) as conn:
        conn.execute('CREATE TABLE crime_2022_2 (DATEEND TEXT, WRONG TEXT)')
    with pytest.raises(ValueError, match='missing'):
        load_records(db)


def test_missing_database_is_not_created(tmp_path):
    path = tmp_path / 'missing.db'
    with pytest.raises(FileNotFoundError):
        load_records(path)
    assert not path.exists()


def test_calendar_exposure_includes_zero_days():
    records = pd.DataFrame({'date': pd.to_datetime(['2020-01-31', '2020-02-29'])})
    summary = calendar_summary(records, '2020-01-01', '2020-02-29', 'day')
    assert summary.loc[31, 'calendar_days'] == 1
    assert summary.loc[29, 'calendar_days'] == 2
    assert summary.loc[29, 'records_per_day'] == 0.5
    assert summary.loc[1, 'records'] == 0


def test_snapshot_reconciliation():
    from pathlib import Path
    path = Path(__file__).parents[1] / 'crime_data.db'
    records, audit = load_records(path)
    assert audit['raw_rows'] == 55851
    assert audit['raw_rows'] == audit['retained_rows'] + audit['excluded_rows']
    part2 = records.loc[records.source_table.eq('crime_2022_2')]
    assert len(part2) > 6000
    assert 'CODE_DEFINED' not in set(records.category)
    assert 'SIMPLE ASSAULT' in set(part2.category)
