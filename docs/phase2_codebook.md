# Phase 2 codebook (RQ2)

**DRAFT — not reviewed.** Fixed before scoring. Changes are logged in
`docs/amendments.md` first.

## How to code

Each of the 6 items gets one code per document:

| Code | Meaning |
|---|---|
| **Disclosed** | The document gives specific information: who, what, when or where, or a named document or reference number. |
| **Partly disclosed** | The topic is mentioned but without the specifics needed to understand or check it. |
| **Not publicly disclosed in reviewed documents** | Nothing on the topic was found in this document. This does **not** mean it does not exist. |

Rules:
- Every code cites the file name and page number(s). "Not publicly disclosed" cites
  the sections searched.
- Code only what the text says. Do not infer from silence or from other projects.
- If text is unclear, choose the lower code and add a note.
- Promises of future action ("will be obtained") are **Partly disclosed** unless the
  document also shows it was done.
- The examples below are made-up wording to show the level. They are not taken
  from any project.

## Items

### 1. Host-country authorisation / NCCC approval
Whether Nigeria's government (e.g. the National Council on Climate Change, or the
Designated National Authority) approved or authorised the project, including any
Article 6 authorisation or letter of approval.

| Code | Example |
|---|---|
| Disclosed | "A Letter of Approval was issued by the Nigerian DNA on 12 March 2021 (ref. DNA/LoA/2021/014), attached as Annex 3." |
| Partly disclosed | "The project has received host country approval." (no issuer, date or reference) |
| Not publicly disclosed in reviewed documents | No mention of government approval or authorisation. |

### 2. Carbon rights
Who owns the emission reductions or credits, and how that ownership was established
(e.g. transfer from households or users to the developer).

| Code | Example |
|---|---|
| Disclosed | "Each household signs a user agreement transferring rights to emission reductions to [developer]; template in Appendix 2." |
| Partly disclosed | "The project proponent holds the rights to the emission reductions." (no basis given) |
| Not publicly disclosed in reviewed documents | No statement on ownership of emission reductions. |

### 3. Benefit-sharing
How revenue from credits, or other benefits, is shared with communities or users.

| Code | Example |
|---|---|
| Disclosed | "15% of net carbon revenue is paid to a community fund managed by [named body]; payments reported annually." |
| Partly disclosed | "Communities benefit from the carbon revenue." or only non-financial benefits listed without any arrangement. |
| Not publicly disclosed in reviewed documents | No mention of sharing revenue or benefits. |

### 4. Community consent
Whether affected communities were consulted and agreed, e.g. a stakeholder
consultation or, where relevant, free, prior and informed consent (FPIC).

| Code | Example |
|---|---|
| Disclosed | "Stakeholder meetings were held in [place] on [date] with 85 participants; comments and responses are summarised in Section E." |
| Partly disclosed | "Local stakeholders were consulted." (no date, place, participants or outcome) |
| Not publicly disclosed in reviewed documents | No mention of consultation or consent. |

### 5. Grievance mechanism
How people affected by the project can raise complaints, and how complaints are handled.

| Code | Example |
|---|---|
| Disclosed | "Complaints can be made by phone at a free number or in a logbook at each distribution point; responses within 30 days; 12 complaints received in this period." |
| Partly disclosed | "A grievance mechanism is in place." (no channel or process) |
| Not publicly disclosed in reviewed documents | No mention of complaints or grievances. |

### 6. Location
Where in Nigeria the project operates.

| Code | Example |
|---|---|
| Disclosed | State(s) and LGA(s) named, or GPS coordinates / a map of the project area. |
| Partly disclosed | Only "Nigeria", a region (e.g. "northern Nigeria"), or "nationwide" without states. |
| Not publicly disclosed in reviewed documents | No location below country level. |

When item 6 is Disclosed, copy the state(s) with page citation into
`state_location` in the register (Phase 1 output).
