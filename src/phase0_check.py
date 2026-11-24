"""Phase 0 data check: what does CarbonPlan OffsetsDB contain about Nigeria?

Reads data/raw/offsets-db.csv.zip directly (no extraction needed), prints a
summary to the console and writes docs/phase0_results.md.

Run from the repo root:
    python src/phase0_check.py
"""

from __future__ import annotations

import json
import zipfile
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ZIP_PATH = ROOT / "data" / "raw" / "offsets-db.csv.zip"
OUT_PATH = ROOT / "docs" / "phase0_results.md"
COUNTRY = "Nigeria"
RETIREMENT_INFO_COLS = [
    "retirement_beneficiary",
    "retirement_beneficiary_harmonized",
    "retirement_account",
    "retirement_reason",
    "retirement_note",
]


def load_tables(zip_path: Path) -> tuple[dict[str, pd.DataFrame], dict]:
    tables: dict[str, pd.DataFrame] = {}
    meta: dict = {}
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            if name.endswith(".csv"):
                tables[Path(name).stem] = pd.read_csv(z.open(name), low_memory=False)
            elif name.endswith("metadata.json"):
                meta = json.loads(z.read(name))
    return tables, meta


def fmt(n: float) -> str:
    return f"{n:,.0f}"


def md_table(df: pd.DataFrame) -> str:
    """Render a DataFrame as a GitHub markdown table (no extra dependency)."""
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for row in df.itertuples(index=False):
        cells = []
        for v in row:
            if isinstance(v, float):
                cells.append(fmt(v))
            else:
                cells.append(str(v).replace("|", "/"))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def count_by(df: pd.DataFrame, col: str) -> pd.DataFrame:
    out = df[col].fillna("(blank)").value_counts().rename_axis(col).reset_index(name="projects")
    return out


def main() -> None:
    tables, meta = load_tables(ZIP_PATH)
    projects = tables["projects"]
    credits = tables["credits"]

    # ---- 1. Tables, columns, row counts ---------------------------------
    print(f"Source: {ZIP_PATH.relative_to(ROOT)}")
    print(f"Metadata: {meta}")
    for name, df in tables.items():
        print(f"\n== {name}: {len(df):,} rows, {df.shape[1]} columns")
        for c in df.columns:
            print(f"   - {c} ({df[c].dtype})")

    # ---- 2. Freshness ----------------------------------------------------
    credits["transaction_date"] = pd.to_datetime(credits["transaction_date"], utc=True, errors="coerce")
    latest_tx = credits["transaction_date"].max()
    generated_at = meta.get("generated_at", "unknown")
    print(f"\nLatest transaction date (all countries): {latest_tx.date()}")
    print(f"Snapshot generated at: {generated_at}")

    # ---- 3. Nigeria filter ----------------------------------------------
    country_norm = projects["country"].astype(str).str.strip()
    ng = projects[country_norm.str.casefold() == COUNTRY.casefold()].copy()
    variants = sorted(set(projects.loc[country_norm.str.contains("nigeria", case=False), "country"]))
    print(f"\nCountry values matching 'nigeria': {variants}")
    print(f"Nigeria projects: {len(ng)}")

    by_registry = count_by(ng, "registry")
    by_category = count_by(ng, "category")
    by_type = count_by(ng, "project_type")
    by_status = count_by(ng, "status")

    totals_registry = (
        ng.groupby("registry", dropna=False)[["issued", "retired"]].sum().reset_index()
        .sort_values("issued", ascending=False)
    )
    totals_category = (
        ng.groupby("category", dropna=False)[["issued", "retired"]].sum().reset_index()
        .sort_values("issued", ascending=False)
    )
    total_issued = ng["issued"].sum()
    total_retired = ng["retired"].sum()

    top10 = (
        ng.sort_values("issued", ascending=False)
        .head(10)[["project_id", "name", "registry", "project_type", "issued", "retired"]]
    )

    # Cross-check project totals against the credits (transactions) table.
    ng_ids = set(ng["project_id"])
    ng_credits = credits[credits["project_id"].isin(ng_ids)]
    tx_types = ng_credits.groupby("transaction_type")["quantity"].agg(["count", "sum"]).reset_index()
    tx_types.columns = ["transaction_type", "transactions", "credits"]
    tx_types["transactions"] = tx_types["transactions"].astype(float)
    ng_latest_tx = ng_credits["transaction_date"].max()
    tx_sum = tx_types.set_index("transaction_type")["credits"]
    tx_issued = tx_sum.get("issuance", 0.0)
    tx_retired = tx_sum[[t for t in tx_sum.index if "retire" in t.lower()]].sum()
    if round(tx_issued) == round(total_issued) and round(tx_retired) == round(total_retired):
        crosscheck_note = (
            "These transaction totals match the project-level issued and retired totals above."
        )
    else:
        crosscheck_note = (
            f"These differ from the project-level totals (issued: {fmt(tx_issued)} vs "
            f"{fmt(total_issued)}; retired: {fmt(tx_retired)} vs {fmt(total_retired)}). "
            "The reason has not yet been investigated."
        )

    # ---- 4. Retirement beneficiary / buyer columns ------------------------
    ng_retirements = ng_credits[ng_credits["transaction_type"].str.contains("retire", case=False, na=False)]
    fill_rows = []
    for col in RETIREMENT_INFO_COLS:
        if col in credits.columns:
            filled = ng_retirements[col].notna() & (ng_retirements[col].astype(str).str.strip() != "")
            n_filled = int(filled.sum())
            share = n_filled / len(ng_retirements) if len(ng_retirements) else 0.0
            credits_filled = ng_retirements.loc[filled, "quantity"].sum()
            fill_rows.append((col, "yes", n_filled, f"{share:.1%}", credits_filled))
        else:
            fill_rows.append((col, "no", 0, "n/a", 0.0))
    fill_df = pd.DataFrame(
        fill_rows,
        columns=["column", "exists", "retirement records filled", "share filled", "credits in filled records"],
    )
    fill_df["retirement records filled"] = fill_df["retirement records filled"].astype(str)

    # ---- Console summary ---------------------------------------------------
    print(f"Nigeria credits issued: {fmt(total_issued)}; retired: {fmt(total_retired)}")
    for title, df in [
        ("By registry", by_registry), ("By category", by_category), ("By project type", by_type),
        ("By status", by_status), ("Credits by registry", totals_registry),
        ("Credits by category", totals_category), ("Top 10 by issued", top10),
        ("Nigeria transactions by type", tx_types), ("Retirement info fill rate", fill_df),
    ]:
        print(f"\n-- {title}\n{df.to_string(index=False)}")

    # ---- 5. Markdown report ------------------------------------------------
    data_date = str(generated_at)[:10]
    report = f"""# Phase 0 results: Nigeria in CarbonPlan OffsetsDB

**DRAFT — not reviewed.** These figures have not been checked against the
original registries. They describe what the dataset contains, not whether any
project or developer is performing well or badly.

*Source: CarbonPlan OffsetsDB (https://carbonplan.org), snapshot generated
{data_date}. OffsetsDB compiles public data from the ACR, ART TREES, Cercarbono,
Climate Action Reserve, Gold Standard, Isometric and Verra registries. Used under
CarbonPlan's Terms of Use; the data is provided "as is". Report produced
{date.today().isoformat()} by `src/phase0_check.py`.*

## 1. What is in the dataset

| table | rows | columns |
|---|---|---|
""" + "\n".join(f"| {n} | {len(df):,} | {df.shape[1]} |" for n, df in tables.items()) + "\n\n" + "\n".join(
        f"- **{n}** columns: " + ", ".join(f"`{c}`" for c in df.columns) for n, df in tables.items()
    ) + f"""

## 2. How recent the data is

- The snapshot was generated on **{data_date}**.
- The latest transaction date in the whole dataset is **{latest_tx.date()}**.
- The latest transaction date for a Nigerian project is **{ng_latest_tx.date() if pd.notna(ng_latest_tx) else "n/a"}**.
- Anything that happened on the registries after the snapshot date is not included.

## 3. Nigeria at a glance

Projects are selected where the `country` field is exactly "{COUNTRY}"
(values found containing "nigeria": {", ".join(variants) or "none"}).

- **{len(ng)} projects** are listed for Nigeria.
- They account for **{fmt(total_issued)} credits issued** and **{fmt(total_retired)} credits retired**
  (from the project-level `issued` and `retired` fields).

### Projects by registry

{md_table(by_registry)}

### Projects by category

{md_table(by_category)}

### Projects by project type

{md_table(by_type)}

### Projects by status

{md_table(by_status)}

## 4. Credits issued and retired

### By registry

{md_table(totals_registry)}

### By category

{md_table(totals_category)}

### Cross-check against the transactions table

The `credits` table records individual transactions. For Nigerian projects it
contains:

{md_table(tx_types)}

{crosscheck_note}

## 5. Top 10 Nigerian projects by credits issued

{md_table(top10)}

## 6. Retirement beneficiary / buyer information

The `credits` table has columns that can record who a retirement was made for.
For the {len(ng_retirements):,} retirement records linked to Nigerian projects,
this is how often each column is filled in:

{md_table(fill_df)}

A blank value means the dataset does not record that information for the
retirement; it does not show whether the information exists elsewhere.

## Next steps

- Check a sample of these figures against the original registry pages.
- Investigate any gaps between project-level totals and transaction totals.
"""
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(report, encoding="utf-8")
    print(f"\nWrote {OUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
