"""Tests for data/processed/nigeria_register.csv (Phase 1, RQ1).

The source totals are recomputed independently from the raw files, so these
tests need data/raw/ to be present; they are skipped otherwise.
Run from the repo root:  python -m pytest -q
"""

import json
import sys
import zipfile
from pathlib import Path

import openpyxl
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import build_register as br  # noqa: E402

CSV = ROOT / "data" / "processed" / "nigeria_register.csv"

pytestmark = pytest.mark.skipif(
    not (CSV.exists() and br.ODB_PATH.exists() and br.BK_PATH.exists()),
    reason="register CSV or raw data missing; run src/build_register.py first",
)


@pytest.fixture(scope="module")
def reg() -> pd.DataFrame:
    return pd.read_csv(CSV)


@pytest.fixture(scope="module")
def odb_source() -> pd.DataFrame:
    """Nigerian projects straight from the OffsetsDB zip (independent of build_register)."""
    with zipfile.ZipFile(br.ODB_PATH) as z:
        p = pd.read_csv(z.open("projects.csv"), low_memory=False)
    return p[p["country"].astype(str).str.strip() == "Nigeria"]


@pytest.fixture(scope="module")
def bk_source() -> pd.DataFrame:
    """Nigerian rows straight from the Berkeley PROJECTS sheet (columns A-Q only)."""
    wb = openpyxl.load_workbook(br.BK_PATH, read_only=True, data_only=True)
    try:
        rows = wb["PROJECTS"].iter_rows(min_row=4, max_col=17, values_only=True)
        header = [" ".join(str(h).split()) for h in next(rows)]
        data = [r for r in rows if r and r[0] is not None]
    finally:
        wb.close()
    df = pd.DataFrame(data, columns=header)
    return df[df["Country"].astype(str).str.strip() == "Nigeria"]


def test_required_columns_present(reg):
    missing = [c for c in br.REQUIRED_COLUMNS if c not in reg.columns]
    assert not missing, f"missing columns: {missing}"


def test_no_duplicate_project_ids(reg):
    dups = reg["project_id"][reg["project_id"].duplicated()].tolist()
    assert not dups, f"duplicate project IDs: {dups}"
    for col in ["offsetsdb_id", "berkeley_id"]:
        ids = reg[col].dropna()
        assert not ids.duplicated().any(), f"duplicate values in {col}"


def test_every_source_project_appears_once(reg, odb_source, bk_source):
    assert set(reg["offsetsdb_id"].dropna()) == set(odb_source["project_id"])
    assert set(reg["berkeley_id"].dropna()) == set(bk_source["Project ID"])


def test_offsetsdb_totals_match_source(reg, odb_source):
    assert reg["issued_offsetsdb"].sum() == pytest.approx(odb_source["issued"].sum())
    assert reg["retired_offsetsdb"].sum() == pytest.approx(odb_source["retired"].sum())


def test_berkeley_totals_match_source(reg, bk_source):
    iss = pd.to_numeric(bk_source["Total Credits Issued"], errors="coerce").fillna(0).sum()
    ret = pd.to_numeric(bk_source["Total Credits Retired"], errors="coerce").fillna(0).sum()
    assert reg["issued_berkeley"].sum() == pytest.approx(iss)
    assert reg["retired_berkeley"].sum() == pytest.approx(ret)


def test_headline_totals_follow_source_rule(reg):
    """Headline figures = Berkeley where present, else OffsetsDB (plan v1.1, Amendment A1)."""
    in_b = reg["in_berkeley"] == "yes"
    expected_iss = reg["issued_berkeley"].where(in_b, reg["issued_offsetsdb"])
    expected_ret = reg["retired_berkeley"].where(in_b, reg["retired_offsetsdb"])
    assert (reg["credits_issued"] == expected_iss).all()
    assert (reg["credits_retired"] == expected_ret).all()
    assert (reg.loc[in_b, "credits_source"] == br.BK_LABEL).all()
    assert (reg.loc[in_b, "credits_as_of"] == br.BK_AS_OF).all()
    assert (reg.loc[~in_b, "credits_source"] == br.ODB_LABEL).all()
    assert reg["credits_source"].notna().all() and reg["credits_as_of"].notna().all()


def test_headline_totals_match_berkeley_source(reg, bk_source):
    """With every project in Berkeley, the headline totals equal Berkeley's Nigeria totals."""
    if (reg["in_berkeley"] == "no").any():
        pytest.skip("some projects are not in Berkeley; covered by the source-rule test")
    iss = pd.to_numeric(bk_source["Total Credits Issued"], errors="coerce").fillna(0).sum()
    ret = pd.to_numeric(bk_source["Total Credits Retired"], errors="coerce").fillna(0).sum()
    assert reg["credits_issued"].sum() == pytest.approx(iss)
    assert reg["credits_retired"].sum() == pytest.approx(ret)


def test_differences_are_consistent(reg):
    both = reg[(reg["in_offsetsdb"] == "yes") & (reg["in_berkeley"] == "yes")]
    assert (both["issued_diff_berkeley_minus_offsetsdb"]
            == both["issued_berkeley"] - both["issued_offsetsdb"]).all()
    assert (both["retired_diff_berkeley_minus_offsetsdb"]
            == both["retired_berkeley"] - both["retired_offsetsdb"]).all()
    one = reg[reg["in_one_source_only"] != "no"]
    assert (one["totals_differ"] == "not compared").all()


def test_state_location_not_yet_filled(reg):
    assert (reg["state_location"] == "not yet reviewed").all()


def test_offsetsdb_snapshot_date(reg):
    with zipfile.ZipFile(br.ODB_PATH) as z:
        as_of = json.loads(z.read("metadata.json"))["generated_at"][:10]
    assert set(reg["offsetsdb_as_of"].dropna()) == {as_of}


@pytest.mark.parametrize("raw, expected", [
    ("GLD7312", "GS7312"), ("GS7312", "GS7312"), ("GS-07312", "GS7312"),
    ("VCS1234", "VCS1234"), ("VERRA1234", "VCS1234"), (" vcs 0042 ", "VCS42"),
])
def test_harmonise_id(raw, expected):
    assert br.harmonise_id(raw) == expected
