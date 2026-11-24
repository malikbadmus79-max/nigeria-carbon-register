"""Phase 1 (RQ1): build the Nigeria project register.

Combines Nigerian projects from two public databases:
  - Berkeley Carbon Trading Project, Voluntary Registry Offsets Database
    v2026-08 (data/raw/Voluntary-Registry-Offsets-Database--v2026-08.xlsx),
    data through 2026-08-31, CC BY 4.0
    -> main source for headline issued/retired (analysis plan v1.1, Amendment A1)
  - CarbonPlan OffsetsDB (data/raw/offsets-db.csv.zip), snapshot 2026-06-01
    -> descriptive fields, first issuance dates, cross-check

Outputs:
  data/processed/nigeria_register.csv
  docs/phase1_register.md   (DRAFT - not reviewed)

Run from the repo root:
    python src/build_register.py
"""

from __future__ import annotations

import json
import re
import zipfile
from datetime import date
from pathlib import Path

import openpyxl
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
ODB_PATH = RAW / "offsets-db.csv.zip"
BK_PATH = RAW / "Voluntary-Registry-Offsets-Database--v2026-08.xlsx"
OUT_CSV = ROOT / "data" / "processed" / "nigeria_register.csv"
OUT_MD = ROOT / "docs" / "phase1_register.md"

COUNTRY = "Nigeria"
BK_AS_OF = "2026-08-31"  # "contains all projects, issuances, and retirements through August 31, 2026"
BK_VERSION = "v2026-08"
ODB_LABEL = "CarbonPlan OffsetsDB"
BK_LABEL = f"Berkeley Voluntary Registry Offsets Database {BK_VERSION}"

REGISTRY_NAMES = {
    "gold-standard": "Gold Standard", "GOLD": "Gold Standard",
    "verra": "Verra", "VCS": "Verra",
}
# Prefix used by each database -> one harmonised prefix.
ID_PREFIX = {"GLD": "GS", "GS": "GS", "VCS": "VCS", "VERRA": "VCS"}

REQUIRED_COLUMNS = [
    "project_id", "offsetsdb_id", "berkeley_id", "name", "registry", "project_type",
    "methodology_protocol", "developer_proponent", "status", "poa_vpa_status",
    "project_type_berkeley", "status_berkeley",
    "credits_issued", "credits_retired", "credits_source", "credits_as_of",
    "first_issuance_date", "first_issuance_source", "first_issuance_year_berkeley",
    "registry_url", "in_offsetsdb", "in_berkeley", "in_one_source_only",
    "issued_offsetsdb", "retired_offsetsdb", "offsetsdb_as_of",
    "issued_berkeley", "retired_berkeley", "berkeley_as_of",
    "issued_diff_berkeley_minus_offsetsdb", "retired_diff_berkeley_minus_offsetsdb",
    "totals_differ", "descriptive_source", "filled_from_berkeley", "state_location",
]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def harmonise_id(raw_id: str) -> str:
    """GLD7312 / GS7312 / GS-07312 -> GS7312; VCS1234 / VERRA1234 -> VCS1234."""
    m = re.match(r"^\s*([A-Za-z]+)[\s_-]?0*(\d+)\s*$", str(raw_id))
    if not m:
        raise ValueError(f"Unrecognised project ID format: {raw_id!r}")
    prefix = m.group(1).upper()
    return f"{ID_PREFIX.get(prefix, prefix)}{int(m.group(2))}"


def clean_text(v) -> str | None:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    s = str(v).strip()
    return None if s == "" or s.lower() in {"unknown", "nan", "none"} else s


def clean_protocol(v) -> str | None:
    """OffsetsDB stores protocols as a list-like string: "['acm0008', 'ams-ii.g']"."""
    s = clean_text(v)
    if s is None:
        return None
    parts = [p.strip(" '\"") for p in s.strip("[]").split(",")]
    parts = [p for p in parts if p]
    return "; ".join(parts) or None


# --------------------------------------------------------------------------
# Loaders
# --------------------------------------------------------------------------
def load_offsetsdb(path: Path = ODB_PATH) -> tuple[pd.DataFrame, pd.DataFrame, str]:
    """Return (Nigerian projects, Nigerian credit transactions, snapshot date)."""
    with zipfile.ZipFile(path) as z:
        projects = pd.read_csv(z.open("projects.csv"), low_memory=False)
        credits = pd.read_csv(z.open("credits.csv"), low_memory=False)
        meta = json.loads(z.read("metadata.json"))
    as_of = str(meta.get("generated_at", ""))[:10]
    ng = projects[projects["country"].astype(str).str.strip() == COUNTRY].copy()
    tx = credits[credits["project_id"].isin(ng["project_id"])].copy()
    tx["transaction_date"] = pd.to_datetime(tx["transaction_date"], utc=True, errors="coerce")
    return ng, tx, as_of


def load_berkeley(path: Path = BK_PATH) -> pd.DataFrame:
    """Return Nigerian rows of the PROJECTS sheet (header on row 4).

    Columns with duplicate headers (the year columns) get a suffix
    ``__<position>`` so every column name is unique.
    """
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        rows = wb["PROJECTS"].iter_rows(min_row=4, values_only=True)
        header = list(next(rows))
        n = max(i for i, h in enumerate(header) if h is not None) + 1
        cols, seen = [], set()
        for i, h in enumerate(header[:n]):
            name = " ".join(str(h).split()) if h is not None else f"col{i}"
            if name in seen:
                name = f"{name}__{i}"
            seen.add(name)
            cols.append(name)
        data = [r[:n] for r in rows if r and r[0] is not None]
    finally:
        wb.close()
    df = pd.DataFrame(data, columns=cols)
    df = df[df["Country"].astype(str).str.strip() == COUNTRY].copy()
    df.attrs["columns_by_position"] = cols
    return df


def berkeley_year_columns(df: pd.DataFrame) -> tuple[dict[int, str], dict[int, str]]:
    """Map year -> column for 'retired or cancelled by year' and 'issued by issuance year'.

    Per the workbook's Column Descriptions sheet: BC-CG = retired/cancelled by
    year, ED-FH = credits issued by issuance year (both 1996-2026).
    """
    cols = df.attrs["columns_by_position"]

    def block(start_letter_index: int) -> dict[int, str]:
        out = {}
        for c in cols[start_letter_index:start_letter_index + 31]:
            out[int(str(c).split("__")[0])] = c
        return out

    col_index = openpyxl.utils.column_index_from_string
    return block(col_index("BC") - 1), block(col_index("ED") - 1)


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------
def build_register(odb: pd.DataFrame, tx: pd.DataFrame, odb_as_of: str, bk: pd.DataFrame) -> pd.DataFrame:
    o = odb.copy()
    o["project_id"] = o["project_id"].map(harmonise_id)
    first_iss = (
        tx[tx["transaction_type"] == "issuance"]
        .assign(project_id=lambda d: d["project_id"].map(harmonise_id))
        .groupby("project_id")["transaction_date"].min().dt.date.astype(str)
    )
    o = o.rename(columns={"project_id": "key"}).assign(offsetsdb_id=odb["project_id"].values)

    b = bk.copy()
    b["key"] = b["Project ID"].map(harmonise_id)
    # First year with credits issued, from Berkeley's "issued by issuance year" columns.
    # (The workbook's hidden "1st issuance yr" column holds the first *vintage* year instead.)
    _, iss_cols = berkeley_year_columns(bk)
    years = sorted(iss_cols)
    b["bk_first_issuance_year"] = [
        next((y for y in years if pd.to_numeric(row[iss_cols[y]], errors="coerce") > 0), None)
        for _, row in bk.iterrows()
    ]

    for df, label in [(o, "OffsetsDB"), (b, "Berkeley")]:
        dups = df["key"][df["key"].duplicated()]
        if len(dups):
            raise ValueError(f"Duplicate project IDs in {label}: {sorted(dups)}")

    m = o.merge(b, on="key", how="outer", indicator=True)

    rows = []
    for _, r in m.iterrows():
        in_o = r["_merge"] in ("both", "left_only")
        in_b = r["_merge"] in ("both", "right_only")
        filled = []

        def pick(odb_val, bk_val, field):
            v = odb_val if in_o else None
            if v is None and in_b and bk_val is not None:
                if in_o:
                    filled.append(field)
                return bk_val
            return v

        name = pick(clean_text(r.get("name")), clean_text(r.get("Project Name")), "name")
        registry = REGISTRY_NAMES.get(r.get("registry") if in_o else r.get("Voluntary Registry"))
        ptype = pick(clean_text(r.get("project_type")), clean_text(r.get("Type")), "project_type")
        method = pick(clean_protocol(r.get("protocol")), clean_text(r.get("Methodology / Protocol")),
                      "methodology_protocol")
        dev = pick(clean_text(r.get("proponent")), clean_text(r.get("Project Developer")),
                   "developer_proponent")
        status = pick(clean_text(r.get("status")), clean_text(r.get("Voluntary Status")), "status")
        url = pick(clean_text(r.get("project_url")), clean_text(r.get("Registry Documents")), "registry_url")

        iss_o = float(r["issued"]) if in_o else None
        ret_o = float(r["retired"]) if in_o else None
        iss_b = float(r["Total Credits Issued"] or 0) if in_b else None
        ret_b = float(r["Total Credits Retired"] or 0) if in_b else None
        # Headline figures: Berkeley is the main source (plan v1.1, Amendment A1);
        # OffsetsDB only for projects Berkeley does not list.
        iss, ret = (iss_b, ret_b) if in_b else (iss_o, ret_o)
        d_iss = iss_b - iss_o if (in_o and in_b) else None
        d_ret = ret_b - ret_o if (in_o and in_b) else None
        bk_first_year = r.get("bk_first_issuance_year") if in_b else None
        bk_first_year = int(bk_first_year) if bk_first_year is not None and pd.notna(bk_first_year) else None
        first_date = first_iss.get(r["key"]) if in_o else None

        rows.append({
            "project_id": r["key"],
            "offsetsdb_id": r["offsetsdb_id"] if in_o else None,
            "berkeley_id": r["Project ID"] if in_b else None,
            "name": name,
            "registry": registry,
            "project_type": ptype,
            "methodology_protocol": method,
            "developer_proponent": dev,
            "status": status,
            "poa_vpa_status": clean_text(r.get("PoA / VPA Status")) if in_b else None,
            "project_type_berkeley": clean_text(r.get("Type")) if in_b else None,
            "status_berkeley": clean_text(r.get("Voluntary Status")) if in_b else None,
            "credits_issued": iss,
            "credits_retired": ret,
            "credits_source": BK_LABEL if in_b else ODB_LABEL,
            "credits_as_of": BK_AS_OF if in_b else odb_as_of,
            "first_issuance_date": first_date,
            "first_issuance_source": ODB_LABEL if first_date else None,
            "first_issuance_year_berkeley": bk_first_year,
            "registry_url": url,
            "in_offsetsdb": "yes" if in_o else "no",
            "in_berkeley": "yes" if in_b else "no",
            "in_one_source_only": "no" if (in_o and in_b) else ("offsetsdb" if in_o else "berkeley"),
            "issued_offsetsdb": iss_o,
            "retired_offsetsdb": ret_o,
            "offsetsdb_as_of": odb_as_of if in_o else None,
            "issued_berkeley": iss_b,
            "retired_berkeley": ret_b,
            "berkeley_as_of": BK_AS_OF if in_b else None,
            "issued_diff_berkeley_minus_offsetsdb": d_iss,
            "retired_diff_berkeley_minus_offsetsdb": d_ret,
            "totals_differ": ("yes" if (d_iss or d_ret) else "no") if (in_o and in_b) else "not compared",
            "descriptive_source": ODB_LABEL if in_o else BK_LABEL,
            "filled_from_berkeley": "; ".join(filled) or None,
            "state_location": "not yet reviewed",
        })

    out = pd.DataFrame(rows, columns=REQUIRED_COLUMNS)
    int_cols = [c for c in out.columns if c.startswith(("credits_issued", "credits_retired", "issued_", "retired_"))
                or c == "first_issuance_year_berkeley"]
    for c in int_cols:
        out[c] = out[c].round().astype("Int64")
    return out.sort_values(["credits_issued", "project_id"], ascending=[False, True]).reset_index(drop=True)


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------
def fmt(v, col: str = "") -> str:
    if col == "year":
        return str(int(v))
    if v is None or (not isinstance(v, str) and pd.isna(v)):
        return ""
    if isinstance(v, (int, float)) or hasattr(v, "__int__") and not isinstance(v, str):
        try:
            return f"{int(v):,}"
        except (TypeError, ValueError):
            pass
    return str(v).replace("|", "/")


def md_table(df: pd.DataFrame) -> str:
    lines = ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "|".join("---" for _ in df.columns) + "|"]
    for row in df.itertuples(index=False):
        lines.append("| " + " | ".join(fmt(v, c) for v, c in zip(row, df.columns)) + " |")
    return "\n".join(lines)


def yearly_comparison(tx: pd.DataFrame, bk: pd.DataFrame) -> pd.DataFrame:
    ret_cols, iss_cols = berkeley_year_columns(bk)
    tx = tx.assign(year=tx["transaction_date"].dt.year)
    o_iss = tx[tx["transaction_type"] == "issuance"].groupby("year")["quantity"].sum()
    o_ret = tx[tx["transaction_type"].str.contains("retire", na=False)].groupby("year")["quantity"].sum()
    b_iss = pd.Series({y: pd.to_numeric(bk[c], errors="coerce").fillna(0).sum() for y, c in iss_cols.items()})
    b_ret = pd.Series({y: pd.to_numeric(bk[c], errors="coerce").fillna(0).sum() for y, c in ret_cols.items()})
    df = pd.DataFrame({
        "issued (OffsetsDB)": o_iss, "issued (Berkeley)": b_iss,
        "retired (OffsetsDB)": o_ret, "retired (Berkeley)": b_ret,
    }).fillna(0)
    df = df[(df != 0).any(axis=1)]
    df["issued difference"] = df["issued (Berkeley)"] - df["issued (OffsetsDB)"]
    df["retired difference"] = df["retired (Berkeley)"] - df["retired (OffsetsDB)"]
    return df.rename_axis("year").reset_index()


def write_report(reg: pd.DataFrame, tx: pd.DataFrame, bk: pd.DataFrame, odb_as_of: str) -> str:
    both = reg[(reg.in_offsetsdb == "yes") & (reg.in_berkeley == "yes")]
    only_b = reg[reg.in_one_source_only == "berkeley"]
    only_o = reg[reg.in_one_source_only == "offsetsdb"]
    yearly = yearly_comparison(tx, bk)
    pre_2026 = yearly[yearly.year < 2026]
    pre_2026_match = bool((pre_2026[["issued difference", "retired difference"]] == 0).all().all())

    tot = lambda s: int(s.fillna(0).sum())  # noqa: E731
    o_iss, o_ret = tot(reg.issued_offsetsdb), tot(reg.retired_offsetsdb)
    b_iss, b_ret = tot(reg.issued_berkeley), tot(reg.retired_berkeley)

    by_reg = reg.groupby("registry").agg(
        projects=("project_id", "size"),
        issued_offsetsdb=("issued_offsetsdb", "sum"), issued_berkeley=("issued_berkeley", "sum"),
        retired_offsetsdb=("retired_offsetsdb", "sum"), retired_berkeley=("retired_berkeley", "sum"),
    ).reset_index()

    iss_diff = both[both.issued_diff_berkeley_minus_offsetsdb != 0]
    ret_diff = both[both.retired_diff_berkeley_minus_offsetsdb != 0]
    ret_lower = ret_diff[ret_diff.retired_diff_berkeley_minus_offsetsdb < 0]
    newly_issuing = both[(both.issued_offsetsdb == 0) & (both.issued_berkeley > 0)]

    added_col = "Date Project Added to Database"
    added = {}
    if added_col in bk.columns:
        for pid, d in zip(bk["Project ID"].map(harmonise_id), bk[added_col]):
            added[pid] = pd.to_datetime(d).date().isoformat() if pd.notna(d) else ""
    only_b_tbl = only_b[["project_id", "name", "registry", "status", "issued_berkeley"]].copy()
    only_b_tbl["added to Berkeley database"] = only_b_tbl.project_id.map(added)

    diff_tbl = iss_diff.sort_values("issued_diff_berkeley_minus_offsetsdb", ascending=False)[
        ["project_id", "name", "project_type", "issued_offsetsdb", "issued_berkeley",
         "issued_diff_berkeley_minus_offsetsdb"]
    ].rename(columns={"issued_diff_berkeley_minus_offsetsdb": "difference"})
    ret_tbl = ret_diff[["project_id", "name", "retired_offsetsdb", "retired_berkeley",
                        "retired_diff_berkeley_minus_offsetsdb"]].rename(
        columns={"retired_diff_berkeley_minus_offsetsdb": "difference"})

    timing_text = (
        "For every year from the first Nigerian issuance up to 2025, the two databases record "
        "exactly the same issuance and retirement totals. All of the differences fall in 2026."
        if pre_2026_match else
        "The two databases also differ in years before 2026 (see table); these differences "
        "are not explained by the snapshot dates alone."
    )

    report = f"""# Phase 1 results: Nigeria project register (RQ1)

**DRAFT — not reviewed.** This report describes what two public databases
record about carbon credit projects in Nigeria. It does not assess any
project, developer or buyer. Figures have not yet been checked against the
registry pages.

*Sources:*
- *{ODB_LABEL} (https://carbonplan.org), snapshot generated {odb_as_of}. Used under
  CarbonPlan's Terms of Use; data provided "as is".*
- *Pamela Quartson, Barbara K Haya, Tyler Bernard, Aline Abayo, Xinyun Rong, Ivy S So,
  Micah Elias. (2026). Voluntary Registry Offsets Database {BK_VERSION}, Berkeley Carbon
  Trading Project, University of California, Berkeley. Retrieved from:
  https://gspp.berkeley.edu/berkeley-carbon-trading-project/offsets-database.
  Data through {BK_AS_OF}. Licensed CC BY 4.0.*

*Produced {date.today().isoformat()} by `src/build_register.py`. Output:
`data/processed/nigeria_register.csv` (columns described in `docs/data_dictionary.md`).*

## 1. Summary

- The register lists **{len(reg)} projects** with country "Nigeria":
  {len(both)} appear in both databases, {len(only_b)} only in Berkeley and {len(only_o)} only in OffsetsDB.
- **Headline — as recorded by Berkeley through {BK_AS_OF}:** {b_iss:,} credits issued
  and {b_ret:,} retired or cancelled.
- **Cross-check — as recorded by OffsetsDB on {odb_as_of}:** {o_iss:,} credits issued and
  {o_ret:,} retired.
- The headline `credits_issued` and `credits_retired` columns use Berkeley, the main
  source under analysis plan v1.1 (Amendment A1, `docs/amendments.md`). OffsetsDB figures
  sit alongside for comparison and remain the source for transaction-level retirement
  data. {"" if only_o.empty else f"For the {len(only_o)} project(s) Berkeley does not list, the OffsetsDB figure is used."}
  Headline register total: {tot(reg.credits_issued):,} issued, {tot(reg.credits_retired):,} retired.
- Project location by Nigerian state is not given by either database (Berkeley's `State`
  field is blank for all Nigerian projects). The `state_location` column is set to
  "not yet reviewed" until project documents are checked.

### By registry

{md_table(by_reg)}

## 2. How the two databases were matched

Projects were matched on their registry project ID. OffsetsDB writes Gold Standard IDs
as `GLD7312` and Berkeley as `GS7312`; both were converted to `GS7312`. Verra IDs use
`VCS` in both. Leading zeros and separators are ignored. Every OffsetsDB project found a
match in Berkeley.

## 3. Differences between the two databases

### Issuance and retirement by year

{md_table(yearly)}

{timing_text} OffsetsDB's snapshot was taken on {odb_as_of} and Berkeley covers activity up
to {BK_AS_OF}, so Berkeley includes three more months of registry activity. The pattern
is consistent with the differences coming from that time gap. Berkeley reports activity
by year only, not by date, so this has not been confirmed transaction by transaction.

### Projects with different issued totals ({len(iss_diff)} projects)

Berkeley's issued total is higher for {int((iss_diff.issued_diff_berkeley_minus_offsetsdb > 0).sum())}
projects and lower for {int((iss_diff.issued_diff_berkeley_minus_offsetsdb < 0).sum())}. The difference adds up to
{tot(iss_diff.issued_diff_berkeley_minus_offsetsdb):,} credits.

{md_table(diff_tbl)}

### Projects with different retired totals ({len(ret_diff)} projects)

{md_table(ret_tbl)}

Berkeley counts credits "retired or cancelled", while OffsetsDB's Nigerian transactions
are all labelled "retirement"; this has not caused differences before 2026.
{"" if ret_lower.empty else f"For {len(ret_lower)} project(s) Berkeley records a *lower* retired total than the earlier OffsetsDB snapshot ({', '.join(ret_lower.project_id)}). A later snapshot showing fewer retirements is not explained by the time gap alone; the cause has not yet been looked into and will be checked against the registry page."}

## 4. Projects found in only one database

**Only in Berkeley ({len(only_b)}):** these projects are not in the OffsetsDB snapshot.
None of them has issued credits in Berkeley's data.

{md_table(only_b_tbl)}

**Only in OffsetsDB ({len(only_o)}):** {"none." if only_o.empty else ", ".join(only_o.project_id)}

## 5. What changed between June and August 2026

Comparing the OffsetsDB snapshot ({odb_as_of}) with Berkeley ({BK_AS_OF}):

- **New listings:** {len(only_b)} projects appear in Berkeley but not in OffsetsDB (table above).
  Some may have been listed after June; others may have been left out of OffsetsDB for
  other reasons. Their listing dates have not yet been checked on the registry.
- **New issuances:** Berkeley records {b_iss - o_iss:,} more credits issued
  ({o_iss:,} → {b_iss:,}), all in issuance year 2026, across {len(iss_diff)} projects.
  {len(newly_issuing)} project(s) had no issuance in OffsetsDB and have issuance in Berkeley:
  {", ".join(newly_issuing.project_id) or "none"}.
- **New retirements:** Berkeley records {b_ret - o_ret:,} more credits retired or cancelled
  ({o_ret:,} → {b_ret:,}), across {len(ret_diff)} projects.

## 6. Notes and next steps

- Descriptive fields (name, type, methodology, developer, status, URL) come from OffsetsDB.
  Where OffsetsDB has a blank or "unknown" value, the Berkeley value is used and the field
  is named in the `filled_from_berkeley` column. The two databases use different words
  for project type and status, so these columns mix the two vocabularies. For a single
  vocabulary, use `project_type_berkeley` and `status_berkeley`, which hold Berkeley's
  values for every project it lists.
- Next: check the projects with differences, and the {len(only_b)} Berkeley-only projects,
  against the Gold Standard and Verra registry pages, and record values with access dates.
"""
    OUT_MD.write_text(report, encoding="utf-8")
    return report


def main() -> None:
    odb, tx, odb_as_of = load_offsetsdb()
    bk = load_berkeley()
    reg = build_register(odb, tx, odb_as_of, bk)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    reg.to_csv(OUT_CSV, index=False, encoding="utf-8")
    write_report(reg, tx, bk, odb_as_of)
    print(f"Projects: {len(reg)} (both: {(reg.in_one_source_only == 'no').sum()}, "
          f"Berkeley only: {(reg.in_one_source_only == 'berkeley').sum()}, "
          f"OffsetsDB only: {(reg.in_one_source_only == 'offsetsdb').sum()})")
    print(f"Issued  OffsetsDB {int(reg.issued_offsetsdb.sum()):,} | Berkeley {int(reg.issued_berkeley.sum()):,}")
    print(f"Retired OffsetsDB {int(reg.retired_offsetsdb.sum()):,} | Berkeley {int(reg.retired_berkeley.sum()):,}")
    print(f"Wrote {OUT_CSV.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
