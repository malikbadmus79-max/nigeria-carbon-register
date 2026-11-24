# Phase 0 results: Nigeria in CarbonPlan OffsetsDB

**DRAFT — not reviewed.** These figures have not been checked against the
original registries. They describe what the dataset contains, not whether any
project or developer is performing well or badly.

*Source: CarbonPlan OffsetsDB (https://carbonplan.org), snapshot generated
2026-06-01. OffsetsDB compiles public data from the ACR, ART TREES, Cercarbono,
Climate Action Reserve, Gold Standard, Isometric and Verra registries. Used under
CarbonPlan's Terms of Use; the data is provided "as is". Report produced
2026-11-24 by `src/phase0_check.py`.*

## 1. What is in the dataset

| table | rows | columns |
|---|---|---|
| credits | 532,799 | 11 |
| projects | 11,659 | 18 |

- **credits** columns: `project_id`, `quantity`, `retirement_account`, `retirement_beneficiary`, `retirement_beneficiary_harmonized`, `retirement_note`, `retirement_reason`, `transaction_date`, `transaction_type`, `transaction_url`, `vintage`
- **projects** columns: `category`, `country`, `first_issuance_at`, `first_retirement_at`, `is_compliance`, `issued`, `listed_at`, `name`, `project_id`, `project_type`, `project_type_source`, `project_url`, `proponent`, `protocol`, `protocol_unassigned`, `registry`, `retired`, `status`

## 2. How recent the data is

- The snapshot was generated on **2026-06-01**.
- The latest transaction date in the whole dataset is **2026-06-01**.
- The latest transaction date for a Nigerian project is **2026-05-29**.
- Anything that happened on the registries after the snapshot date is not included.

## 3. Nigeria at a glance

Projects are selected where the `country` field is exactly "Nigeria"
(values found containing "nigeria": Nigeria).

- **129 projects** are listed for Nigeria.
- They account for **13,540,409 credits issued** and **6,172,553 credits retired**
  (from the project-level `issued` and `retired` fields).

### Projects by registry

| registry | projects |
|---|---|
| gold-standard | 116 |
| verra | 13 |

### Projects by category

| category | projects |
|---|---|
| unknown | 99 |
| energy-efficiency | 18 |
| renewable-energy | 6 |
| forest | 4 |
| agriculture | 2 |

### Projects by project type

| project_type | projects |
|---|---|
| Clean Water | 68 |
| Cookstove | 33 |
| Unknown | 16 |
| Distributed Solar | 4 |
| Afforestation + Reforestation | 2 |
| Wetland | 2 |
| Sustainable Agriculture | 1 |
| REDD+ | 1 |
| Electric Vehicle | 1 |
| Energy Efficiency | 1 |

### Projects by status

| status | projects |
|---|---|
| unknown | 98 |
| listed | 27 |
| registered | 4 |

## 4. Credits issued and retired

### By registry

| registry | issued | retired |
|---|---|---|
| gold-standard | 13,311,538 | 6,113,373 |
| verra | 228,871 | 59,180 |

### By category

| category | issued | retired |
|---|---|---|
| unknown | 8,607,532 | 3,224,985 |
| energy-efficiency | 4,932,877 | 2,947,568 |
| agriculture | 0 | 0 |
| forest | 0 | 0 |
| renewable-energy | 0 | 0 |

### Cross-check against the transactions table

The `credits` table records individual transactions. For Nigerian projects it
contains:

| transaction_type | transactions | credits |
|---|---|---|
| issuance | 335 | 13,540,409 |
| retirement | 1,424 | 6,172,553 |

These transaction totals match the project-level issued and retired totals above.

## 5. Top 10 Nigerian projects by credits issued

| project_id | name | registry | project_type | issued | retired |
|---|---|---|---|---|---|
| GLD7312 | Promoting Improved Cooking practices in Nigeria | gold-standard | Cookstove | 4,358,255 | 2,854,604 |
| GLD11671 | GS10789 GS11671 VPA61: Efficient and Clean  Cooking for households in Nigeria | gold-standard | Cookstove | 1,598,549 | 369,390 |
| GLD11306 | Improved Cookstove  Programme - Nigeria - VPA 48 | gold-standard | Cookstove | 321,507 | 0 |
| GLD11265 | Safe Water Programme – Nigeria – VPA 07 | gold-standard | Clean Water | 222,723 | 123,057 |
| GLD11279 | Safe Water Programme – Nigeria – VPA 21 | gold-standard | Clean Water | 214,642 | 53,213 |
| GLD11263 | Safe Water Programme – Nigeria – VPA 05 | gold-standard | Clean Water | 206,234 | 129,775 |
| GLD11280 | Safe Water Programme – Nigeria – VPA 22 | gold-standard | Clean Water | 199,836 | 65,088 |
| GLD11273 |  Safe Water Programme – Nigeria – VPA 15 | gold-standard | Clean Water | 197,852 | 122,085 |
| GLD11266 | Safe Water Programme – Nigeria – VPA 08 | gold-standard | Clean Water | 196,011 | 84,719 |
| GLD11270 |  Safe Water Programme – Nigeria – VPA 12 | gold-standard | Clean Water | 195,408 | 77,091 |

## 6. Retirement beneficiary / buyer information

The `credits` table has columns that can record who a retirement was made for.
For the 1,424 retirement records linked to Nigerian projects,
this is how often each column is filled in:

| column | exists | retirement records filled | share filled | credits in filled records |
|---|---|---|---|---|
| retirement_beneficiary | yes | 898 | 63.1% | 5,559,027 |
| retirement_beneficiary_harmonized | yes | 12 | 0.8% | 120,090 |
| retirement_account | yes | 0 | 0.0% | 0 |
| retirement_reason | yes | 3 | 0.2% | 59,180 |
| retirement_note | yes | 713 | 50.1% | 1,282,004 |

A blank value means the dataset does not record that information for the
retirement; it does not show whether the information exists elsewhere.

## Next steps

- Check a sample of these figures against the original registry pages.
- Investigate any gaps between project-level totals and transaction totals.
