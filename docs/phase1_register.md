# Phase 1 results: Nigeria project register (RQ1)

**DRAFT — not reviewed.** This report describes what two public databases
record about carbon credit projects in Nigeria. It does not assess any
project, developer or buyer. Figures have not yet been checked against the
registry pages.

*Sources:*
- *CarbonPlan OffsetsDB (https://carbonplan.org), snapshot generated 2026-06-01. Used under
  CarbonPlan's Terms of Use; data provided "as is".*
- *Pamela Quartson, Barbara K Haya, Tyler Bernard, Aline Abayo, Xinyun Rong, Ivy S So,
  Micah Elias. (2026). Voluntary Registry Offsets Database v2026-08, Berkeley Carbon
  Trading Project, University of California, Berkeley. Retrieved from:
  https://gspp.berkeley.edu/berkeley-carbon-trading-project/offsets-database.
  Data through 2026-08-31. Licensed CC BY 4.0.*

*Produced 2026-11-24 by `src/build_register.py`. Output:
`data/processed/nigeria_register.csv` (columns described in `docs/data_dictionary.md`).*

## 1. Summary

- The register lists **137 projects** with country "Nigeria":
  129 appear in both databases, 8 only in Berkeley and 0 only in OffsetsDB.
- **Headline — as recorded by Berkeley through 2026-08-31:** 18,372,530 credits issued
  and 6,246,028 retired or cancelled.
- **Cross-check — as recorded by OffsetsDB on 2026-06-01:** 13,540,409 credits issued and
  6,172,553 retired.
- The headline `credits_issued` and `credits_retired` columns use Berkeley, the main
  source under analysis plan v1.1 (Amendment A1, `docs/amendments.md`). OffsetsDB figures
  sit alongside for comparison and remain the source for transaction-level retirement
  data. 
  Headline register total: 18,372,530 issued, 6,246,028 retired.
- Project location by Nigerian state is not given by either database (Berkeley's `State`
  field is blank for all Nigerian projects). The `state_location` column is set to
  "not yet reviewed" until project documents are checked.

### By registry

| registry | projects | issued_offsetsdb | issued_berkeley | retired_offsetsdb | retired_berkeley |
|---|---|---|---|---|---|
| Gold Standard | 120 | 13,311,538 | 18,143,659 | 6,113,373 | 6,186,848 |
| Verra | 17 | 228,871 | 228,871 | 59,180 | 59,180 |

## 2. How the two databases were matched

Projects were matched on their registry project ID. OffsetsDB writes Gold Standard IDs
as `GLD7312` and Berkeley as `GS7312`; both were converted to `GS7312`. Verra IDs use
`VCS` in both. Leading zeros and separators are ignored. Every OffsetsDB project found a
match in Berkeley.

## 3. Differences between the two databases

### Issuance and retirement by year

| year | issued (OffsetsDB) | issued (Berkeley) | retired (OffsetsDB) | retired (Berkeley) | issued difference | retired difference |
|---|---|---|---|---|---|---|
| 2011 | 1,867 | 1,867 | 0 | 0 | 0 | 0 |
| 2013 | 17,320 | 17,320 | 0 | 0 | 0 | 0 |
| 2014 | 2,328 | 2,328 | 0 | 0 | 0 | 0 |
| 2015 | 18,162 | 18,162 | 0 | 0 | 0 | 0 |
| 2017 | 71,504 | 71,504 | 0 | 0 | 0 | 0 |
| 2018 | 85,530 | 85,530 | 0 | 0 | 0 | 0 |
| 2020 | 770,783 | 770,783 | 62 | 62 | 0 | 0 |
| 2021 | 1,822,312 | 1,822,312 | 221,779 | 221,779 | 0 | 0 |
| 2022 | 2,124,456 | 2,124,456 | 1,553,149 | 1,553,149 | 0 | 0 |
| 2023 | 1,521,456 | 1,521,456 | 1,140,185 | 1,140,185 | 0 | 0 |
| 2024 | 3,202,164 | 3,202,164 | 1,489,817 | 1,489,817 | 0 | 0 |
| 2025 | 2,323,359 | 2,323,359 | 1,357,018 | 1,357,018 | 0 | 0 |
| 2026 | 1,579,168 | 6,411,289 | 410,543 | 484,018 | 4,832,121 | 73,475 |

For every year from the first Nigerian issuance up to 2025, the two databases record exactly the same issuance and retirement totals. All of the differences fall in 2026. OffsetsDB's snapshot was taken on 2026-06-01 and Berkeley covers activity up
to 2026-08-31, so Berkeley includes three more months of registry activity. The pattern
is consistent with the differences coming from that time gap. Berkeley reports activity
by year only, not by date, so this has not been confirmed transaction by transaction.

### Projects with different issued totals (65 projects)

Berkeley's issued total is higher for 65
projects and lower for 0. The difference adds up to
4,832,121 credits.

| project_id | name | project_type | issued_offsetsdb | issued_berkeley | difference |
|---|---|---|---|---|---|
| GS11671 | GS10789 GS11671 VPA61: Efficient and Clean  Cooking for households in Nigeria | Cookstove | 1,598,549 | 3,384,325 | 1,785,776 |
| GS12505 | GS10789 GS 11673 RVPA-65: Efficient and Clean Cooking for households in Nigeria | Cookstove | 0 | 185,574 | 185,574 |
| GS12406 | Safe Water Programme – Nigeria - VPA 90 | Clean Water | 25,904 | 82,915 | 57,011 |
| GS12410 | Safe Water Programme – Nigeria - VPA 94 | Clean Water | 18,710 | 74,993 | 56,283 |
| GS12405 | Safe Water Programme – Nigeria - VPA 89 | Clean Water | 28,304 | 84,105 | 55,801 |
| GS12411 | Safe Water Programme – Nigeria - VPA 95 | Clean Water | 19,228 | 74,981 | 55,753 |
| GS12402 | Safe Water Programme – Nigeria - VPA 86 | Clean Water | 27,601 | 83,254 | 55,653 |
| GS12409 | Safe Water Programme – Nigeria - VPA 93 | Clean Water | 20,519 | 75,960 | 55,441 |
| GS12115 | GS7591 VPA 51 Safe Water Supply in Nigeria | Clean Water | 0 | 54,989 | 54,989 |
| GS12401 | Safe Water Programme – Nigeria - VPA 85 | Clean Water | 28,913 | 83,647 | 54,734 |
| GS12404 | Safe Water Programme – Nigeria - VPA 88 | Clean Water | 28,210 | 82,813 | 54,603 |
| GS12407 | Safe Water Programme – Nigeria - VPA 91 | Clean Water | 25,706 | 80,272 | 54,566 |
| GS12414 | Safe Water Programme – Nigeria - VPA 98 | Clean Water | 17,080 | 71,087 | 54,007 |
| GS12399 | Safe Water Programme – Nigeria - VPA 83 | Clean Water | 27,916 | 81,555 | 53,639 |
| GS12412 | Safe Water Programme – Nigeria - VPA 96 | Clean Water | 18,398 | 71,621 | 53,223 |
| GS12415 | Safe Water Programme – Nigeria - VPA 99 | Clean Water | 15,330 | 68,534 | 53,204 |
| GS12400 | Safe Water Programme – Nigeria - VPA 84 | Clean Water | 27,657 | 80,564 | 52,907 |
| GS12416 | Safe Water Programme – Nigeria - VPA 100 | Clean Water | 15,180 | 67,876 | 52,696 |
| GS12417 | Safe Water Programme – Nigeria - VPA 101 | Clean Water | 14,750 | 66,803 | 52,053 |
| GS12403 | Safe Water Programme – Nigeria - VPA 87 | Clean Water | 26,783 | 78,798 | 52,015 |
| GS12398 | Safe Water Programme – Nigeria - VPA 82 | Clean Water | 28,707 | 80,608 | 51,901 |
| GS11273 | Safe Water Programme – Nigeria – VPA 15 | Clean Water | 197,852 | 249,298 | 51,446 |
| GS11265 | Safe Water Programme – Nigeria – VPA 07 | Clean Water | 222,723 | 274,142 | 51,419 |
| GS12413 | Safe Water Programme – Nigeria - VPA 97 | Clean Water | 18,648 | 69,975 | 51,327 |
| GS12393 | Safe Water Programme – Nigeria - VPA 77 | Clean Water | 43,372 | 94,486 | 51,114 |
| GS12391 | Safe Water Programme – Nigeria - VPA 75 | Clean Water | 45,152 | 95,533 | 50,381 |
| GS11277 | Safe Water Programme – Nigeria – VPA 19 | Clean Water | 194,957 | 245,221 | 50,264 |
| GS12392 | Safe Water Programme – Nigeria - VPA 76 | Clean Water | 42,976 | 92,981 | 50,005 |
| GS12408 | Safe Water Programme – Nigeria - VPA 92 | Clean Water | 23,338 | 73,217 | 49,879 |
| GS11279 | Safe Water Programme – Nigeria – VPA 21 | Clean Water | 214,642 | 263,587 | 48,945 |
| GS12394 | Safe Water Programme – Nigeria - VPA 78 | Clean Water | 41,290 | 89,959 | 48,669 |
| GS12390 | Safe Water Programme – Nigeria - VPA 74 | Clean Water | 47,160 | 95,548 | 48,388 |
| GS12395 | Safe Water Programme – Nigeria - VPA 79 | Clean Water | 35,403 | 83,494 | 48,091 |
| GS11276 | Safe Water Programme – Nigeria – VPA 18 | Clean Water | 194,259 | 242,085 | 47,826 |
| GS12396 | Safe Water Programme – Nigeria - VPA 80 | Clean Water | 35,834 | 83,009 | 47,175 |
| GS11280 | Safe Water Programme – Nigeria – VPA 22 | Clean Water | 199,836 | 246,763 | 46,927 |
| GS12397 | Safe Water Programme – Nigeria - VPA 81 | Clean Water | 31,326 | 78,197 | 46,871 |
| GS11272 | Safe Water Programme – Nigeria – VPA 14 | Clean Water | 181,300 | 227,991 | 46,691 |
| GS11282 | Safe Water Programme – Nigeria – VPA 24 | Clean Water | 179,250 | 225,834 | 46,584 |
| GS11275 | Safe Water Programme – Nigeria – VPA 17 | Clean Water | 192,852 | 238,982 | 46,130 |
| GS11263 | Safe Water Programme – Nigeria – VPA 05 | Clean Water | 206,234 | 251,705 | 45,471 |
| GS11274 | Safe Water Programme – Nigeria – VPA 16 | Clean Water | 183,111 | 228,221 | 45,110 |
| GS11268 | Safe Water Programme – Nigeria – VPA 10 | Clean Water | 192,742 | 237,316 | 44,574 |
| GS11278 | Safe Water Programme – Nigeria – VPA 20 | Clean Water | 194,728 | 238,410 | 43,682 |
| GS11271 | Safe Water Programme – Nigeria – VPA 13 | Clean Water | 164,004 | 207,536 | 43,532 |
| GS11281 | Safe Water Programme – Nigeria – VPA 23 | Clean Water | 181,682 | 224,388 | 42,706 |
| GS11270 | Safe Water Programme – Nigeria – VPA 12 | Clean Water | 195,408 | 237,929 | 42,521 |
| GS11260 | Safe Water Programme – Nigeria – VPA 02 | Clean Water | 186,474 | 227,774 | 41,300 |
| GS12418 | Safe Water Programme – Nigeria - VPA 102 | Clean Water | 10,451 | 51,505 | 41,054 |
| GS11286 | Safe Water Programme – Nigeria – VPA 28 | Clean Water | 162,796 | 202,613 | 39,817 |
| GS11283 | Safe Water Programme – Nigeria – VPA 25 | Clean Water | 184,667 | 223,476 | 38,809 |
| GS11269 | Safe Water Programme – Nigeria – VPA 11 | Clean Water | 184,898 | 223,038 | 38,140 |
| GS11266 | Safe Water Programme – Nigeria – VPA 08 | Clean Water | 196,011 | 233,871 | 37,860 |
| GS11267 | Safe Water Programme – Nigeria – VPA 09 | Clean Water | 189,471 | 227,198 | 37,727 |
| GS11261 | Safe Water Programme – Nigeria – VPA 03 | Clean Water | 187,834 | 225,317 | 37,483 |
| GS11285 | Safe Water Programme – Nigeria – VPA 27 | Clean Water | 183,236 | 220,552 | 37,316 |
| GS11284 | Safe Water Programme – Nigeria – VPA 26 | Clean Water | 179,357 | 216,581 | 37,224 |
| GS11259 | Safe Water Programme – Nigeria – VPA 01 | Clean Water | 186,752 | 221,788 | 35,036 |
| GS11264 | Safe Water Programme – Nigeria – VPA 06 | Clean Water | 158,406 | 192,860 | 34,454 |
| GS11288 | Safe Water Programme – Nigeria – VPA 30 | Clean Water | 179,958 | 213,967 | 34,009 |
| GS11262 | Safe Water Programme – Nigeria – VPA 04 | Clean Water | 180,766 | 214,495 | 33,729 |
| GS11210 | UpEnergy-Social and Climate Impact Programme- Cooking Devices VPA-8 | Cookstove | 0 | 31,969 | 31,969 |
| GS11287 | Safe Water Programme – Nigeria – VPA 29 | Clean Water | 102,741 | 130,207 | 27,466 |
| GS12665 | Crescendo Safe Water Supply 2 | Clean Water | 0 | 7,276 | 7,276 |
| GS12213 | Crescendo Safe Water Supply | Clean Water | 0 | 3,895 | 3,895 |

### Projects with different retired totals (4 projects)

| project_id | name | retired_offsetsdb | retired_berkeley | difference |
|---|---|---|---|---|
| GS7312 | Promoting Improved Cooking practices in Nigeria | 2,854,604 | 2,924,928 | 70,324 |
| GS11671 | GS10789 GS11671 VPA61: Efficient and Clean  Cooking for households in Nigeria | 369,390 | 373,996 | 4,606 |
| GS11274 | Safe Water Programme – Nigeria – VPA 16 | 96,158 | 94,513 | -1,645 |
| GS11271 | Safe Water Programme – Nigeria – VPA 13 | 87,929 | 88,119 | 190 |

Berkeley counts credits "retired or cancelled", while OffsetsDB's Nigerian transactions
are all labelled "retirement"; this has not caused differences before 2026.
For 1 project(s) Berkeley records a *lower* retired total than the earlier OffsetsDB snapshot (GS11274). A later snapshot showing fewer retirements is not explained by the time gap alone; the cause has not yet been looked into and will be checked against the registry page.

## 4. Projects found in only one database

**Only in Berkeley (8):** these projects are not in the OffsetsDB snapshot.
None of them has issued credits in Berkeley's data.

| project_id | name | registry | status | issued_berkeley | added to Berkeley database |
|---|---|---|---|---|---|
| GS13004 | GS12943 GS12944 RVPA1 Oyu - Building Sustainable Nigerian Communities VPA02 | Gold Standard | Listed | 0 | 2026-08-31 |
| GS23569 | GS10963-UpEnergy -Social and Climate Impact Programme -Safe Water Drinking Programme- VPA 56 | Gold Standard | Listed | 0 | 2026-08-31 |
| GS23585 | Vinasse Waste Management - Biogas Application | Gold Standard | Listed | 0 | 2026-08-31 |
| GS23699 | GS10789-GS11673-RVPA-121: Efficient and Clean Cooking for households in Nigeria | Gold Standard | Listed | 0 | 2026-08-31 |
| VCS3624 | Clean Cookstove Project | Verra | Pipeline listing requested (under development) | 0 | 2026-08-31 |
| VCS5729 | Federal University of Oye-Ekiti Virtual Power Plant (FUOYE's VPP) | Verra | Pipeline listing requested (under validation) | 0 | 2026-08-31 |
| VCS5946 | Recovery and marketing of gas that would otherwise be flared at the OML 24, Nigeria | Verra | Under validation (Public comment period closed) | 0 | 2026-08-31 |
| VCS6026 | Spitfire Flare Gas Conservation Project | Verra | Pipeline listing (under development) approved | 0 | 2026-06-30 |

**Only in OffsetsDB (0):** none.

## 5. What changed between June and August 2026

Comparing the OffsetsDB snapshot (2026-06-01) with Berkeley (2026-08-31):

- **New listings:** 8 projects appear in Berkeley but not in OffsetsDB (table above).
  Some may have been listed after June; others may have been left out of OffsetsDB for
  other reasons. Their listing dates have not yet been checked on the registry.
- **New issuances:** Berkeley records 4,832,121 more credits issued
  (13,540,409 → 18,372,530), all in issuance year 2026, across 65 projects.
  5 project(s) had no issuance in OffsetsDB and have issuance in Berkeley:
  GS12505, GS12115, GS11210, GS12665, GS12213.
- **New retirements:** Berkeley records 73,475 more credits retired or cancelled
  (6,172,553 → 6,246,028), across 4 projects.

## 6. Notes and next steps

- Descriptive fields (name, type, methodology, developer, status, URL) come from OffsetsDB.
  Where OffsetsDB has a blank or "unknown" value, the Berkeley value is used and the field
  is named in the `filled_from_berkeley` column. The two databases use different words
  for project type and status, so these columns mix the two vocabularies. For a single
  vocabulary, use `project_type_berkeley` and `status_berkeley`, which hold Berkeley's
  values for every project it lists.
- Next: check the projects with differences, and the 8 Berkeley-only projects,
  against the Gold Standard and Verra registry pages, and record values with access dates.
