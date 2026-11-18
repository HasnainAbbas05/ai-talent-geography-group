# Data dictionary and reproducibility guide

**Project:** Global AI Talent Flow — *Do countries that train AI researchers retain them, or does talent concentrate in a few destination countries?*  
**Intended audience:** Government policy analysts comparing the training, retention and employment affiliations of AI researchers.  
**Data package location:** `data/` in the GitHub repository.  
**Dataset snapshot:** NeurIPS 2025 authors with complete career histories; workplaces observed in **2026**.  
**Source charts retrieved:** **24 October 2026**. The retrieval date is not the workplace observation date.

## 1. Source, provenance and licence

**Original study**  
Ma, D., & Yang, B. (2026, September 23). *Who's ahead in the global AI talent race?* Carnegie Endowment for International Peace.

- [Original study and methodology](https://carnegieendowment.org/features/whos-ahead-in-the-global-ai-talent-race)
- [Published PDF report](https://assets.carnegieendowment.org/files/Ma_AI%20Talent-2026.pdf)
- [Mobility counts — Flourish chart 30265299](https://public.flourish.studio/visualisation/30265299/embed?1355501)
- [Retention and undergraduate training — Flourish chart 30285922](https://public.flourish.studio/visualisation/30285922/embed?1355501)
- [Selected undergraduate → graduate → workplace pathways — Flourish chart 30286797](https://public.flourish.studio/visualisation/30286797/embed?1355501)

**What was collected.** The three public Flourish charts embedded in the Carnegie study contain aggregate figures. Their published numerical tables were read from the public chart data on **24 October 2026** and preserved in `published_chart_data.json`. No values were estimated by measuring chart pixels. The source JSON is a *saved copy of public chart data*, **not** Carnegie's individual-level research database or an official downloadable Carnegie CSV. The four CSV files in this package are processed extracts of that saved snapshot.

**Licence / rights status (for all five data files below):** The [Carnegie study](https://carnegieendowment.org/features/whos-ahead-in-the-global-ai-talent-race) displays **© 2026 Carnegie Endowment for International Peace. All rights reserved.** No explicit Creative Commons or other open-data licence for these particular chart data tables was identified. The charts being publicly viewable in [Flourish](https://flourish.studio/terms/) does **not** by itself establish an unrestricted right to redistribute their contents. Accordingly, the licence is recorded as **“No explicit open-data licence identified; Carnegie copyright applies; reuse permissions not independently established.”** The processed CSVs retain attribution to the originating study; changing their format does not create a new licence for the underlying source data. Check any redistribution or public-repository permissions with the rights holder or teaching team where necessary. This is a record of the identified rights status, **not** a claim of permission or legal advice.

**Time coverage across the package:** One **2025 conference cohort**, with **2026 workplace affiliations**; researchers' individual undergraduate and graduate education dates vary and are **not supplied** as a year-by-year time series. The **latest observation available in this package is the 2026 workplace snapshot** (no exact observation day/month is provided). The data were **retrieved on 24 October 2026**, not refreshed live in the Streamlit app.

### Files and their roles

| File in `data/` | Records | Type | Source / processing role |
|---|---:|---|---|
| `published_chart_data.json` | Three charts (11 + 11 + 18 rows) | Preserved source sample | Snapshot of the three public Flourish chart tables and source metadata. |
| `published_retention.csv` | 11 | Processed CSV | Cleans the retention chart's undergraduate totals and published percentages. |
| `published_mobility.csv` | 11 | Processed CSV | Cleans the mobility chart's leaving and arriving counts; computes net difference. |
| `selected_career_paths.csv` | 18 | Processed CSV | Copies **only** the 18 career paths selected for publication. |
| `ai_talent_country_summary.csv` | 11 | Processed CSV | Joins retention and mobility by geography and derives retained, working and net totals. |
| `build_data.mjs` | — | Transformation script, **not a dataset** | Rebuilds all four CSVs from `published_chart_data.json` and runs assertions. |
| `README.md` | — | Documentation | This data dictionary and reproducibility guide. |

**Common conventions:** A *count* is a number of researchers (people) in the observed subset. A *percentage* uses the **0–100 scale**, not a 0–1 fraction; “pp” means percentage points. `country_or_region` is the publisher's classification: **Europe** and **Other** are grouped regions rather than individual countries. The UK is separate from Europe; Hong Kong is counted with China. URLs are source references, not measured variables.

## 2. Dataset dictionary — `ai_talent_country_summary.csv`

- **Role:** Main application dataset for comparing undergraduate education and 2026 work locations, retention and workforce composition.
- **Source / URLs:** Derived from [retention chart 30285922](https://public.flourish.studio/visualisation/30285922/embed?1355501) and [mobility chart 30265299](https://public.flourish.studio/visualisation/30265299/embed?1355501); original publisher is Carnegie Endowment (study linked in Section 1).
- **Licence:** No explicit open-data licence identified; Carnegie copyright / reuse-status note in Section 1 applies.
- **Rows / primary key:** 11 rows; **`country_or_region`** is unique within this fixed 2025/2026 snapshot. For a multi-cohort extension, use `(conference_cohort_year, workplace_observation_year, country_or_region)`.
- **Time coverage / latest observation:** 2025 NeurIPS cohort; latest observed workplace affiliation **2026**; retrieval **24 October 2026**. Undergraduate education years are not supplied.
- **Transformation:** The Node script matches the 11 geographic labels in the two published tables and calculates retained, working, net and retention measures as specified below. See Section 7.

| Column | Type / units | Definition and derivation |
|---|---|---|
| `conference_cohort_year` | Integer; calendar year | **2025**, the NeurIPS accepted-paper cohort. |
| `workplace_observation_year` | Integer; calendar year | **2026**, the workplace observation year. |
| `country_or_region` | String; geography label | The published country/region grouping; primary key for this snapshot. |
| `geography_type` | Categorical text; no units | `country` or `grouped_region`; Europe and Other are grouped. |
| `undergraduate_educated_count` | Integer; researchers | Publisher's “Own graduates”: undergraduate institution in this geography. |
| `working_outside_origin_group_count` | Integer; researchers | Publisher's “Left”: undergraduate geography here, 2026 workplace geography elsewhere. |
| `same_origin_work_group_count` | Integer; researchers | **Retained = undergraduate_educated_count − working_outside_origin_group_count**. Same published geography at undergraduate and workplace stages. |
| `educated_elsewhere_working_here_count` | Integer; researchers | Publisher's “Arrived”: undergraduate geography elsewhere, workplace geography here. |
| `work_destination_count` | Integer; researchers | **Working = same_origin_work_group_count + educated_elsewhere_working_here_count**. |
| `net_difference_count` | Signed integer; researchers | **Net = educated_elsewhere_working_here_count − working_outside_origin_group_count = work_destination_count − undergraduate_educated_count**. |
| `published_retention_percent` | Number; % (0–100), 1 decimal | Publisher's displayed retention percentage. |
| `recalculated_retention_percent` | Number; % (0–100), 6 decimals | **100 × same_origin_work_group_count / undergraduate_educated_count**. Additional decimal places are arithmetic precision, not additional certainty. |
| `retention_source_url` | URL text; no units | The public retention source chart. |
| `mobility_source_url` | URL text; no units | The public mobility source chart. |

## 3. Dataset dictionary — `published_retention.csv`

- **Role:** Source-aligned retention table used to audit undergraduate counts and retention percentages.
- **Source / URL:** [Carnegie's public retention Flourish chart 30285922](https://public.flourish.studio/visualisation/30285922/embed?1355501).
- **Licence:** No explicit open-data licence identified; see Section 1.
- **Rows / primary key:** 11; unique **`country_or_region`** for this snapshot.
- **Time coverage / latest observation:** NeurIPS **2025** cohort, workplace observation **2026**, source retrieved **24 October 2026**. These dates come from the package/study; this CSV intentionally has no year column.
- **Transformation:** Read chart's `Country/region`, `Own graduates` and numeric `Retention Bar`; remove thousands separators in counts; preserve published one-decimal retention and append source URL. The visual display-only `Retention` text is not separately included.

| Column | Type / units | Definition |
|---|---|---|
| `country_or_region` | String; geography label | Published country or grouped region; primary key. |
| `undergraduate_educated_count` | Integer; researchers | Number whose undergraduate institution was in this geography (“Own graduates”). |
| `published_retention_percent` | Number; % (0–100), 1 decimal | Publisher's rounded percentage of those graduates whose workplace is in the same published geography in 2026. |
| `source_url` | URL text; no units | Link to the public retention Flourish chart. |

## 4. Dataset dictionary — `published_mobility.csv`

- **Role:** Source-aligned leaving, arriving and net-difference counts.
- **Source / URL:** [Carnegie's public mobility Flourish chart 30265299](https://public.flourish.studio/visualisation/30265299/embed?1355501).
- **Licence:** No explicit open-data licence identified; see Section 1.
- **Rows / primary key:** 11; unique **`country_or_region`** for this snapshot.
- **Time coverage / latest observation:** NeurIPS **2025** cohort, workplace observation **2026**, source retrieved **24 October 2026**. These dates are package metadata rather than columns in this CSV.
- **Transformation:** Extract `Country/region`, `Left` and `Arrived` from source rows; calculate **net_difference_count = arrived_count − left_count** and add the source URL. The source's signed `Net` display string and positive/negative bar-display columns are not retained, because the numeric difference is recalculated.

| Column | Type / units | Definition |
|---|---|---|
| `country_or_region` | String; geography label | Publisher's country or grouped region; primary key. |
| `left_count` | Integer; researchers | Researchers trained at undergraduate level here but working in a different published geography in 2026. |
| `arrived_count` | Integer; researchers | Researchers trained at undergraduate level elsewhere but working here in 2026. |
| `net_difference_count` | Signed integer; researchers | **arrived_count − left_count**; a cross-geography affiliation comparison, not verified migration. |
| `source_url` | URL text; no units | Link to the public mobility Flourish chart. |

## 5. Dataset dictionary — `selected_career_paths.csv`

- **Role:** A *selected*, incomplete set of published undergraduate → graduate → work pathways used by the Where They Work visualisation.
- **Source / URL:** [Carnegie's public selected-pathways Flourish chart 30286797](https://public.flourish.studio/visualisation/30286797/embed?1355501).
- **Licence:** No explicit open-data licence identified; see Section 1.
- **Rows / primary key:** 18; composite key **(`undergraduate_country_or_region`, `graduate_country_or_region`, `work_country_or_region`)** is unique in this published snapshot. Add the two year columns to the key if combined with other cohorts.
- **Time coverage / latest observation:** NeurIPS **2025** cohort; workplace affiliation **2026**; source retrieved **24 October 2026**. Individual undergraduate/graduate years are not recorded.
- **Transformation:** Copy the three stage labels and `People` counts from the publisher's 18 selected rows; add cohort year, workplace year, coverage warning and source URL. The chart's redundant `People Bar` display field is not exported. **Do not interpret missing pathways as zero counts.**

| Column | Type / units | Definition |
|---|---|---|
| `conference_cohort_year` | Integer; calendar year | **2025**, NeurIPS accepted-paper cohort. |
| `workplace_observation_year` | Integer; calendar year | **2026**, observed workplace year. |
| `undergraduate_country_or_region` | String; geography label | Published undergraduate-stage geography. |
| `graduate_country_or_region` | String; geography label / category | Published graduate-stage geography; includes the special category `No grad school` for some rows. |
| `work_country_or_region` | String; geography label | Published workplace-stage geography in 2026. |
| `researcher_count` | Integer; researchers | Published `People` count for the specific three-stage combination. |
| `coverage` | Explanatory text; no units | Indicates these are **18 selected published pathways**, not a complete flow matrix. |
| `source_url` | URL text; no units | Link to the public pathways Flourish chart. |

**Coverage caution:** These 18 rows sum to **8,214** researchers (**79.9%** of the 10,280-person complete-history sample); the remaining **2,066** researchers have no specified three-stage pathway in this *published selection*. An unlisted flow is **unknown, not zero**. The dashboard's grey “origin not published” category is calculated as the published aggregate arrival count minus the origins identifiable from selected published pathways; it is not a guessed country allocation.

## 6. Dataset dictionary — `published_chart_data.json` (preserved source sample)

- **Role:** Raw-in-package source sample from which all four CSVs can be regenerated. It is **not** researcher-level data.
- **Source / URLs:** The three public Flourish chart URLs in Section 1, associated with the Carnegie study.
- **Licence:** No explicit open-data licence identified; see Section 1.
- **Structure / keys:** One JSON object containing metadata and a `charts` mapping with **three chart IDs**: `30265299`, `30285922`, `30286797`. Each chart has `url`, `title`, `columns` and `rows`.
- **Primary key:** At JSON chart level, the chart ID is unique. For a specific source row, `(chart ID, row index)` locates it in the preserved snapshot (row index is its position, starting at zero). Within charts 30265299 and 30285922, `Country/region` is unique; within chart 30286797, `(Undergraduate, Graduate, Works in)` is unique for this snapshot. A row index is a *snapshot locator*, not a stable identifier across future releases.
- **Time coverage / latest observation:** Metadata records **2025** cohort and **2026** workplace observation. Original study published **23 September 2026** and public chart data retrieved **24 October 2026**. There is no finer observation date or per-person timeline.
- **Transformation:** No analytical transformation to the preserved JSON; it stores the source headers/rows and retrieval metadata. `build_data.mjs` reads it and creates the four processed CSVs. Some source columns are display-specific and are not carried into the CSV files.

### JSON metadata dictionary

| Key | Type / units | Meaning |
|---|---|---|
| `publisher` | Text; no units | Carnegie Endowment for International Peace. |
| `authors` | Array of text; no units | Source authors Damien Ma and Binyi Yang. |
| `study_title` | Text; no units | Published study title. |
| `study_url` | URL text; no units | Original study page. |
| `publication_date` | ISO date (`YYYY-MM-DD`) | **2026-09-23**, publication date. |
| `retrieved_date` | ISO date (`YYYY-MM-DD`) | **2026-10-24**, chart data retrieval date, not a new research observation. |
| `conference_cohort_year` | Integer; calendar year | **2025** NeurIPS conference cohort. |
| `workplace_observation_year` | Integer; calendar year | **2026** employment snapshot. |
| `charts` | Object keyed by chart ID; no units | The three Flourish source tables. |
| `charts[ID].url` | URL text; no units | That chart's public source URL. |
| `charts[ID].title` | Text; no units | That chart's published title. |
| `charts[ID].columns` | Ordered text array; no units | Column names corresponding by position to every row array. |
| `charts[ID].rows` | Array of row arrays; mixed units | Original published values in the same order as `columns`. |

### Source chart columns and units

| Chart ID and role | Source columns (in order) | Units / treatment |
|---|---|---|
| `30265299` — mobility, 11 rows | `Country/region`; `Left`; `Arrived`; `Net`; `Net Positive`; `Net Negative` | Geography text; researchers; researchers; signed count displayed as text; positive count or null (display); negative count or null (display). The script uses `Left` and `Arrived` to calculate net numerically. |
| `30285922` — retention, 11 rows | `Country/region`; `Own graduates`; `Retention`; `Retention Bar` | Geography text; researcher count formatted as text with commas; percentage formatted as text; numeric percentage on the 0–100 scale. Script uses `Own graduates` and numeric `Retention Bar`. |
| `30286797` — selected career paths, 18 rows | `Undergraduate`; `Graduate`; `Works in`; `People`; `People Bar` | Three categorical geography/stage labels; researcher count; redundant numeric count for chart display. Script uses the first four fields. |

## 7. Reproduce the processed CSV files

### Requirements

- The repository `data/` folder must contain `published_chart_data.json` and `build_data.mjs` **with these exact filenames**.
- Install **Node.js** (no extra npm packages are required by this script).
- Run the command below **from the repository root**:

```bash
node data/build_data.mjs
```

This overwrites or creates the following files **inside `data/`** using the preserved source snapshot:

```text
data/ai_talent_country_summary.csv
data/published_retention.csv
data/published_mobility.csv
data/selected_career_paths.csv
```

The script uses `node:fs`, `node:path` and `node:assert/strict`; it does not download live data. Re-running it produces the same fixed snapshot until the preserved JSON or script changes. The program prints a JSON summary of its checks.

### Transformation and validation flow

1. Read the three source-chart tables from `published_chart_data.json` by chart ID.
2. Convert comma-formatted undergraduate counts to integers and preserve published one-decimal retention percentages.
3. Join retention rows to mobility rows by identical `Country/region` names.
4. Compute **retained = trained − left**, **working = retained + arrived**, **net = arrived − left**, and **retention (%) = 100 × retained / trained**.
5. Tag Europe and Other as `grouped_region`; tag all other published geography rows as `country`.
6. Export the 18 published career paths without inferring the unpublished flows.
7. Assert consistency and write the four CSVs with the schemas documented in Sections 2–5.

The included script checks the following expected results:

| Integrity check | Expected result |
|---|---:|
| Unique published geography rows | 11 |
| Undergraduate counts summed over all geography groups | 10,280 |
| Derived workplace counts summed over all geography groups | 10,280 |
| Sum of net differences | 0 |
| Recalculated retention, rounded to one decimal | Matches each published retention percentage |
| Selected published career path rows | 18 |
| Selected career path people total | 8,214 |

**Concrete recomputation:** In the USA row, the published undergraduate count is **1,369** and the number working in another published geography is **155**. Therefore **retained = 1,369 − 155 = 1,214** and **retention = 1,214 / 1,369 × 100 = 88.677867…%**, or **88.7%** at the publisher's rounding precision. Mobility also shows **2,300** researchers trained elsewhere but working in the USA; the derived workplace total is **1,214 + 2,300 = 3,514**, and **net = 2,300 − 155 = +2,145**.

**Verification note:** The reconstruction from the uploaded source snapshot and script was tested against the four supplied CSVs and they matched. If any input files are changed after this documented snapshot, rerun the script and checks before committing the assessed version.

## 8. Data boundaries and responsible interpretation

- **Selected population, not all AI researchers:** 10,280 authors of NeurIPS 2025 accepted papers with complete undergraduate, graduate and workplace histories, approximately 40% of the conference's unique authors. This is not a random sample of all AI researchers or all NeurIPS authors.
- **Undergraduate geography is not nationality:** Country of undergraduate institution must not be called citizenship, birthplace, or a verified domestic/foreign person's status. In the dashboard, “homegrown” means **undergraduate affiliation in the same published geography**; “imported” means **undergraduate affiliation elsewhere**, not a legal immigration category.
- **Workplace affiliation is not proof of relocation:** Institution or employer country does not necessarily locate the person's physical office; “left,” “arrived” and “retained” are snapshot affiliation comparisons, not observed immigration histories.
- **Grouped regions are not countries:** Europe and Other combine multiple countries. Matching undergraduate and workplace *groups* does not mean staying in one country. Do not silently merge those grouped rows into country rankings.
- **One snapshot, not a trend:** The 2025 conference cohort with workplaces observed in 2026 cannot by itself show annual growth/decline or establish that a policy caused a difference.
- **Small denominators:** Australia, Singapore and Russia each have fewer than 100 undergraduate-affiliated researchers in the observed sample; percentages for small groups need caution.
- **Incomplete published career-path combinations:** Only 18 selected paths, covering 8,214 people, are available; a missing path is not evidence of a zero flow. Any “unpublished destination/origin” segment is the difference between known aggregate totals and disclosed paths.
- **Source uncertainty:** Carnegie notes that profile data are self-maintained and that Europe's direction can be sensitive to sample selection. The group cannot verify each individual record from these aggregate tables.

## 9. Relationship to the Streamlit app

The updated application presents **Overview**, **1 · Train vs work**, **2 · Size vs retention**, **3 · Where they work**, **4 · Workforce Composition**, and **Data and limits**. These tabs use the same underlying country summary and (where relevant) the selected published career paths. The Overview is a dashboard of these four perspectives; it is not a separate dataset.

- **Train vs work:** Differences between workplace and undergraduate affiliations, displayed as counts or shares of the 10,280-person sample.
- **Size vs retention:** Undergraduate cohort size compared with retention; grouped regions should be distinguished from individual countries.
- **Where they work:** Employer-side breakdown using aggregate retained counts plus the selected published paths; any unlisted origins remain grouped as unknown.
- **Workforce Composition:** Derived same-geography versus elsewhere-educated workplace counts. These terms refer to education/work affiliations, not citizenship or migration status.
- **Data and limits:** Attribution, scope, source date and interpretation cautions.

If app tab names or analyses change again, update this section to match the assessed commit. The data package does **not** by itself satisfy the separate course requirements for a member-by-member **AI provenance matrix** or a **Data and AI disclosure statement**; those must be supplied and verified separately.

## 10. Reference

Ma, D., & Yang, B. (2026, September 23). *Who's ahead in the global AI talent race?* Carnegie Endowment for International Peace. https://carnegieendowment.org/features/whos-ahead-in-the-global-ai-talent-race
