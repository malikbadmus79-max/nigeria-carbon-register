# Data Dictionary — `data/processed/nigeria_register.csv`

**DRAFT — not reviewed.** Built by `src/build_register.py` (Phase 1, RQ1).
One row per project. Licence for this file: CC BY 4.0 (see `LICENSE-DATA.md`).

**Sources**
- **Berkeley** = Berkeley Carbon Trading Project, Voluntary Registry Offsets Database
  v2026-08 (data through 2026-08-31), CC BY 4.0. Main source for headline credits
  issued and retired (`docs/analysis_plan.md` v1.1, Amendment A1).
- **OffsetsDB** = CarbonPlan OffsetsDB, snapshot generated 2026-06-01. Source for
  descriptive fields and first issuance dates, and used as a cross-check.

Projects are included if the source's country field is exactly "Nigeria".
Credits are counted in tonnes of CO2-equivalent as recorded by the registries
(1 credit = 1 tCO2e nominal). Blank cells mean the source has no value.

## Identification

| Column | Type | Description |
|---|---|---|
| `project_id` | text | Harmonised registry project ID used to match the two databases. Gold Standard IDs are written `GS<number>` (OffsetsDB's `GLD7312` → `GS7312`); Verra IDs `VCS<number>`. Leading zeros removed. Unique per row. |
| `offsetsdb_id` | text | Project ID exactly as written in OffsetsDB (e.g. `GLD7312`). Blank if not in OffsetsDB. |
| `berkeley_id` | text | Project ID exactly as written in Berkeley (e.g. `GS7312`). Blank if not in Berkeley. |

## Descriptive fields

Taken from OffsetsDB. If OffsetsDB's value is blank or "unknown", the Berkeley
value is used instead and the column name is listed in `filled_from_berkeley`.
For projects only in Berkeley, all descriptive fields come from Berkeley.

| Column | Type | Description |
|---|---|---|
| `name` | text | Project name as recorded on the registry. |
| `registry` | text | Registry that issues the credits: "Gold Standard" or "Verra" (harmonised from OffsetsDB `gold-standard`/`verra` and Berkeley `GOLD`/`VCS`). |
| `project_type` | text | Project type. OffsetsDB's classification (e.g. "Cookstove", "Clean Water"); Berkeley's wording where filled from Berkeley (e.g. "Cookstoves"). The two vocabularies are mixed in this column. |
| `methodology_protocol` | text | Methodology/protocol. OffsetsDB codes (e.g. `gs-tpddtec`), several separated by `; `; Berkeley's full methodology name where filled from Berkeley. |
| `developer_proponent` | text | Project developer / proponent as recorded in the source. |
| `status` | text | Project status. OffsetsDB values ("listed", "registered") or, where OffsetsDB says "unknown", Berkeley's voluntary status (e.g. "Gold Standard Certified Project"). Mixed vocabularies. |
| `poa_vpa_status` | text | From Berkeley only: whether the project is a Programme of Activities ("POA"), a component of a programme ("VPA"), or "Standalone". |
| `project_type_berkeley` | text | Berkeley's project type for every project it lists (single vocabulary). |
| `status_berkeley` | text | Berkeley's "Voluntary Status" for every project it lists (single vocabulary). |
| `registry_url` | text | Link to the project's registry page (OffsetsDB `project_url`; Berkeley `Registry Documents` where filled from Berkeley). |
| `descriptive_source` | text | Main source of the descriptive fields for this row. |
| `filled_from_berkeley` | text | Columns where OffsetsDB was blank/"unknown" and the Berkeley value was used, separated by `; `. Blank if none. |

## Headline figures

| Column | Type | Description |
|---|---|---|
| `credits_issued` | integer | Total credits issued. Berkeley value if the project is in Berkeley, otherwise OffsetsDB (Amendment A1). |
| `credits_retired` | integer | Total credits retired. Berkeley value ("retired or cancelled") if the project is in Berkeley, otherwise OffsetsDB (Amendment A1). |
| `credits_source` | text | Source of `credits_issued` and `credits_retired`. |
| `credits_as_of` | date | Date of the source data for the headline figures (2026-06-01 for OffsetsDB, 2026-08-31 for Berkeley). |
| `first_issuance_date` | date | Date of the project's earliest issuance transaction in OffsetsDB's `credits` table. Blank if OffsetsDB records no issuance. |
| `first_issuance_source` | text | Source of `first_issuance_date`. |
| `first_issuance_year_berkeley` | integer | First year with credits issued, from Berkeley's "Credits issued by issuance year" columns. (Not Berkeley's hidden "1st issuance yr" column, which holds the first vintage year.) |
| `state_location` | text | Nigerian state(s) where the project operates, as stated in project documents. Currently "not yet reviewed" for all rows; neither database gives this (Berkeley's `State` field is blank for Nigeria). Filled in after document review, with page citation. |

## Source coverage and cross-check

| Column | Type | Description |
|---|---|---|
| `in_offsetsdb` | yes/no | Project appears in the OffsetsDB snapshot. |
| `in_berkeley` | yes/no | Project appears in Berkeley's PROJECTS sheet. |
| `in_one_source_only` | text | "no" if in both; otherwise the one source it appears in ("offsetsdb" or "berkeley"). |
| `issued_offsetsdb` | integer | Credits issued per OffsetsDB (project-level `issued`). Blank if not in OffsetsDB. |
| `retired_offsetsdb` | integer | Credits retired per OffsetsDB (project-level `retired`). Blank if not in OffsetsDB. |
| `offsetsdb_as_of` | date | OffsetsDB snapshot date (2026-06-01). |
| `issued_berkeley` | integer | Credits issued per Berkeley ("Total Credits Issued"; excludes buffer pool and Gold Standard PERs). Blank if not in Berkeley. |
| `retired_berkeley` | integer | Credits retired or cancelled per Berkeley ("Total Credits Retired"). Blank if not in Berkeley. |
| `berkeley_as_of` | date | Last date covered by Berkeley v2026-08 (2026-08-31). |
| `issued_diff_berkeley_minus_offsetsdb` | integer | `issued_berkeley` − `issued_offsetsdb`. Blank unless in both. |
| `retired_diff_berkeley_minus_offsetsdb` | integer | `retired_berkeley` − `retired_offsetsdb`. Blank unless in both. |
| `totals_differ` | text | "yes" if either difference is non-zero, "no" if both are zero, "not compared" if the project is in only one source. |

A difference between the two databases is not an error in either. The snapshots
are three months apart (see `docs/phase1_register.md`).
