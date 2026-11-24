# Phase 2 document sample (RQ2)

**DRAFT — not reviewed.** Set on 2026-11-24, before any scoring, under
`docs/analysis_plan.md` v1.1. Any change to the sample is logged in
`docs/amendments.md` first.

Figures: credits issued as recorded by the Berkeley Voluntary Registry Offsets
Database v2026-08 (through 2026-08-31), from `data/processed/nigeria_register.csv`.
Programme (PoA) IDs are from the same Berkeley file.

## Rule

1. Rank Nigerian projects by `credits_issued`. Take projects from the top until
   they cover at least 70% of the total.
2. Group them by shared programme (PoA). A programme document counts once for all
   its sub-projects (VPAs).
3. For each group, take:
   - **Standalone project:** PDD, latest monitoring report, latest verification report.
   - **Programme:** the PoA design document, plus the VPA design document, latest
     monitoring report and latest verification report for these VPAs:
     - the largest VPA of each project type in the group, and
     - the smallest VPA in the group within the 70% set (to see whether documents
       vary across VPAs).
4. Add a small **pipeline** group: the two gas-flare projects listed on Verra
   (VCS5946, VCS6026). Take the latest project description for each.
5. Keep the total to about 20 documents. "Latest" means the most recent version on
   the registry on the day of download; record the date in `docs/sources/README.md`.

## Result

24 projects reach 71.1% of 18,372,530 credits issued. They fall into 3 groups.

| Group | Projects in 70% set | Credits issued | Documents |
|---|---|---|---|
| A. GS7312 (standalone, cookstoves) | 1 | 4,358,255 | 3 |
| B. Programme GS10789 (cookstoves) | 1 (VPA GS11671) | 3,384,325 | 4 |
| C. Programme GS11189 (safe water + 1 cookstove VPA) | 22 | 5,314,053 | 10 |
| D. Pipeline (gas flare, Verra) | – | 0 | 2 |
| **Total** | **24** | **13,056,633** | **19** |

VPAs chosen in group C:
- **GS11306**, VPA 48: the largest cookstove VPA, with 321,507 credits.
- **GS11265**, VPA 07: the largest safe-water VPA, with 274,142 credits.
- **GS11269**, VPA 11: the smallest VPA in the 70% set, with 223,038 credits.

The other 19 safe-water VPAs in the 70% set are covered at programme level through
the GS11189 programme document. Their scores are not reported separately.

## Notes

- Berkeley lists GS11306 (a cookstove VPA) under programme GS11189 (safe water).
  Confirm this on the registry page when downloading. If it belongs to a different
  programme, log the change before scoring.
- Programme pages GS10789 and GS11189 are not in the Nigerian register (a programme
  may cover several countries). Their links in the download list are built in the
  same format as the other Gold Standard links.
