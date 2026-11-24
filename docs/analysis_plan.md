# Analysis Plan — Nigeria Carbon Register

**Version 1.1 · DRAFT — not reviewed** (Draft status lasts until Phase 5 review is complete.)

*v1.1 includes Amendment A1 (2026-11-24): Berkeley v2026-08 becomes the main
source for headline issued/retired totals. See `docs/amendments.md`.*

This plan sets out what the project will analyse, how, and under which rules,
before the main analysis starts. Once frozen (see `docs/plan_freeze.md`), any
change is logged in `docs/amendments.md` before it is applied.

## Starting point (from Phase 0)

According to CarbonPlan OffsetsDB (snapshot generated 2026-06-01; see
`docs/phase0_results.md`):

- 129 projects are listed with country "Nigeria" (116 Gold Standard, 13 Verra).
- 73 projects have issued credits. Together they record 13,540,409 credits issued
  and 6,172,553 retired.
- All recorded issuance comes from two project types: Cookstove (7,191,616
  credits, 53.1%) and Clean Water (6,348,793 credits, 46.9%).
- The 20 largest issuing projects together account for at least 70% of credits
  issued for Nigeria.
- Category and status are "unknown" for most projects (99 and 98 of 129).
- 63.1% of the 1,424 Nigerian retirement records have the
  `retirement_beneficiary` field filled.

These figures describe the dataset only and are subject to the Phase 5 review.

---

## 1. Research questions

**RQ1 — Register.** What is publicly visible about Nigeria's carbon credit
projects: project list, project type, registry, status, credits issued and
retired, and the Nigerian state(s) where project documents say the project
operates?

**RQ2 — Transparency.** For the top projects by credits issued, and a sample of
about 20 project documents, what is publicly disclosed about:
1. host-country authorisation / National Council on Climate Change (NCCC) approval
2. carbon rights (who holds the rights to the emission reductions)
3. benefit-sharing arrangements
4. community consent (e.g. stakeholder consultation, FPIC where relevant)
5. grievance mechanism
6. project location (state, LGA or coordinates)

**RQ3 — Integrity sensitivity.** For the cookstove and clean-water projects that
together account for at least 70% of Nigerian credits issued, how do the credits
issued compare with a conservative range calculated from published alternative
parameter values (e.g. fraction of non-renewable biomass (fNRB), usage or
adoption rates, fuel savings / water-boiling baselines)? Results are reported by
method and project type, not as verdicts on named projects.

**RQ4 — Buyers.** Where the public retirement beneficiary field is filled, which
organisations retire credits from Nigerian projects, and in what volumes and years?

**RQ5 — Policy.** Which fields should Nigeria's national carbon registry
record, compared with the registries or regulatory frameworks of Ghana and Kenya?

---

## 2. Data

| Source | Use | Storage |
|---|---|---|
| Berkeley Carbon Trading Project — Voluntary Registry Offsets Database v2026-08 (CC BY 4.0, data through 2026-08-31) | Main source for headline credits issued and retired per project (RQ1, RQ3) *(A1)* | `data/raw/` (gitignored) |
| CarbonPlan OffsetsDB, snapshot generated 2026-06-01 | Transaction-level issuance and retirement data, including retirement beneficiary fields (RQ4); first issuance dates; cross-check of Berkeley totals *(A1)* | `data/raw/` (gitignored) |
| Gold Standard and Verra registry pages | Updates after June 2026; cross-check selected figures | Figures recorded with access date |
| Gold Standard / Verra project documents (PDD, monitoring reports, verification reports), downloaded by hand, max ~20 | RQ2 disclosure scoring; RQ3 parameter values used in the credited calculations | `docs/sources/` (gitignored); a source list (file name, URL, access date) is tracked in the repo |
| Nigerian policy documents (e.g. Climate Change Act 2021, National Carbon Market Activation Policy / framework, NCCC guidance) | RQ2 authorisation context; RQ5 | `docs/sources/` |
| Ghana and Kenya registry / carbon market regulations | RQ5 comparison | `docs/sources/` |
| Published literature and methodology documents (e.g. peer-reviewed studies on cookstove and water-treatment crediting, Gold Standard / CDM default values, ICVCM assessments) | RQ3 alternative parameter values | Cited in full; PDFs in `docs/sources/` |

Rules for data:
- Raw and third-party files stay in `data/raw/` or `docs/sources/` and are not
  redistributed. Only our own derived outputs go in `data/processed/` (CC BY 4.0).
- Every figure records its source and the date it was recorded.
- Registry pages may change; each value taken from them is stored with its access
  date.

---

## 3. Methods

### RQ1 — Register
1. Take Nigerian projects (country = "Nigeria") from both Berkeley v2026-08 and
   OffsetsDB, and match them by harmonised registry project ID.
2. Headline credits issued and retired come from Berkeley (data through
   2026-08-31) *(A1)*. For a project that appears only in OffsetsDB, the OffsetsDB
   figure is used and labelled as such. Both sources' figures are kept side by side
   in the register.
3. Cross-check Berkeley totals against OffsetsDB (project-level and year-by-year);
   list and explain any difference instead of resolving it silently.
4. Check registry pages for projects with activity after 2026-08-31, and for
   differences between the two databases, and record values separately with their
   access date.
5. Add the Nigerian state(s) only where a project document states them, with page
   citation. Otherwise record "not stated in reviewed documents".
6. Output: `data/processed/nigeria_register.csv` plus a data dictionary.

### RQ2 — Transparency scorecard
1. **Sample:** the top projects by credits issued, plus a sample of documents
   totalling about 20. Where several projects (VPAs) share one programme (PoA)
   document, that document counts once. Record how the sample was chosen before
   scoring.
2. **Coding scheme:** for each of the six items, code one of: *Disclosed*
   (specific information given), *Partly disclosed* (mentioned without specifics),
   *Not publicly disclosed in reviewed documents*. Each code must cite the
   document and page. Write the codebook with examples before scoring starts.
3. **AI-assisted first pass:** an AI model extracts candidate answers and page
   citations from each document.
4. **100% manual check:** a person checks every AI answer against the cited page,
   then confirms, corrects or rejects it. Record the AI answer, the final answer
   and whether it was changed, and report the AI–human agreement rate.
5. Output: scorecard by item and project type. The project-level scorecard is
   published with citations and contains only "disclosed / not disclosed" codes,
   no ratings or rankings of developers.

### RQ3 — Integrity sensitivity
1. **Scope:** cookstove and clean-water projects, taken in descending order of
   credits issued until they reach at least 70% of Nigerian issuance (about 20
   projects per Phase 0).
2. **Credited parameters:** record from monitoring and verification reports the
   parameter values used in the credited calculation (e.g. fNRB, usage rate,
   fuel consumption baseline/project, share of households boiling water, emission
   factors), with page citations.
3. **Alternative values:** collect alternative values only from published
   sources (peer-reviewed studies, official methodology defaults, recognised
   assessments). Each value is cited; for each parameter, set a central and a
   conservative alternative and note how relevant it is to Nigeria.
4. **Calculation:** recalculate emission reductions under the alternative values,
   holding everything else as reported, to give a range per method/project type.
   Show one-at-a-time sensitivity (which parameter matters most) and a combined
   conservative case.
5. **Reporting:** results are aggregated by methodology and project type and
   described as "screening sensitivity estimates". No project-specific
   over-crediting figure is headlined, and no global over-crediting multiplier is
   applied to Nigeria.
6. Code and parameter tables are published so others can reproduce or challenge
   the range.

### RQ4 — Buyers
1. Use Nigerian retirement records from the OffsetsDB `credits` table (snapshot
   2026-06-01; Berkeley has no transaction-level beneficiary data) *(A1)* where
   `retirement_beneficiary` (or `retirement_beneficiary_harmonized`) is filled.
   Report the share of Berkeley's retired total covered by these records.
2. Normalise organisation names by hand (log every mapping) and classify each
   beneficiary as organisation, individual or unclear.
3. Report organisations by volume and year, with the share of retirements that
   have no beneficiary recorded. Individuals and unclear entries are reported
   only as aggregate counts and volumes.
4. Use `retirement_note` only to classify retirements, never to name individuals.

### RQ5 — Policy comparison
1. Build a field list from: data used in RQ1–RQ4, Article 6 / Paris Agreement
   reporting needs (authorisation, corresponding adjustments, first transfer),
   and what the Ghana and Kenya frameworks require or publish.
2. Compare Nigeria, Ghana and Kenya field by field, coded as *required / published
   / not found in reviewed documents*, with citations.
3. Output: a recommended minimum field set for a Nigerian national registry, each
   field linked to the gap it addresses.

---

## 4. Phases

| Phase | Work | Main outputs |
|---|---|---|
| 0 (done) | Data check | `docs/phase0_results.md` |
| 1 | Register build (RQ1) | `data/processed/nigeria_register.csv`, data dictionary, cross-check note |
| 2 | Transparency scorecard (RQ2) | Codebook, document source list, scorecard with citations, AI–human agreement log |
| 3 | Integrity sensitivity (RQ3) | Parameter tables, sensitivity code, results by method/project type |
| 4 | Buyers and policy comparison (RQ4, RQ5) | Buyer tables (organisations only), field comparison, recommended field set |
| 5 | Audit and review | Independent check of a sample of figures and codes; corrections log; right of reply offered to named registries/developers before publication; DRAFT label removed only after this phase |
| 6 | Communication | Dashboard, policy brief, social media carousel, all following the safe-claim rules |

---

## 5. Safe-claim rules (binding)

These rules apply to every output, including drafts, charts, social posts and
the dashboard.

1. **Describe, don't allege.** State what public data shows. Never allege fraud,
   wrongdoing, greenwashing or bad faith by any project, developer, registry or buyer.
2. **Absence of disclosure is not absence.** "Not publicly disclosed" never means
   "does not exist". Always write "not publicly disclosed in the documents
   reviewed (as of [date])".
3. **Integrity results are screening estimates.** RQ3 results are "screening
   sensitivity estimates", not corrections or findings of over-crediting. Never
   apply a global over-crediting multiplier to Nigeria.
4. **Buyers.** Name an organisation as a buyer only if it appears in the public
   registry beneficiary field. Individuals are aggregated and never named.
5. **Dated and sourced.** Every figure is "as recorded on [date]" with its source.
6. **Draft until reviewed.** Everything is marked DRAFT until the Phase 5 review
   is complete.

---

## 6. Limits and what would change the plan

**Known limits**
- OffsetsDB is a snapshot (2026-06-01). It covers only the registries it
  collects and may miss projects listed elsewhere (e.g. other standards, Article 6
  bilateral deals, or projects not yet on any registry).
- Projects are selected by the country field "Nigeria". Multi-country programmes
  or projects with a different country label may be missed.
- Category and status are "unknown" for most Nigerian projects in OffsetsDB, so
  status analysis depends on the registry pages.
- About 20 documents cannot represent all 129 projects; RQ2 findings apply to the
  sample reviewed.
- The beneficiary field is filled for 63.1% of Nigerian retirement records; RQ4
  describes only those records.
- Sensitivity ranges depend on which published values exist; there may be few
  that are specific to Nigeria.
- Public documents may not reflect agreements that exist privately; this is why
  rule 2 applies.
- AI-assisted extraction can miss or misread text; the full manual check is meant
  to catch this but does not guarantee completeness.

**What would change the plan** (any change is logged in `docs/amendments.md` first)
- A newer OffsetsDB snapshot or registry data that changes which projects reach
  the 70% threshold.
- New project types issuing credits in Nigeria (e.g. forestry, renewable energy).
- Publication of a Nigerian national registry, NCCC authorisation list, or new
  carbon market regulations.
- Big differences between OffsetsDB, Berkeley and registry pages that need a change
  to the main data source.
- Documents being unavailable, so the sample has to change.
- Reviewer feedback in Phase 5.
