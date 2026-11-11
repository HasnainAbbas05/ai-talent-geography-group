# AI researcher education, employment and retention: usable aggregate data

Prepared for the question: Do countries that train AI researchers retain them, or does their talent concentrate in a few destination countries?

Suggested audience: a government policy analyst assessing the education, retention and attraction of AI research talent.

## Source and access

Ma, D., & Yang, B. (2026, September 23). Who’s ahead in the global AI talent race? Carnegie Endowment for International Peace.

Study and methodology: https://carnegieendowment.org/features/whos-ahead-in-the-global-ai-talent-race

Public report: https://assets.carnegieendowment.org/files/Ma_AI%20Talent-2026.pdf

The publisher embeds the following public Flourish tables in that study. This package extracts their published numeric data; it is not the authors' individual-level research database and is not an official Carnegie CSV release.

- Mobility counts: https://public.flourish.studio/visualisation/30265299/embed?1355501
- Retention and undergraduate education totals: https://public.flourish.studio/visualisation/30285922/embed?1355501
- Selected three-stage career paths: https://public.flourish.studio/visualisation/30286797/embed?1355501

Accessed 24 October 2026. The values were read from the public chart HTML's JSON data, not estimated from chart pixels. `published_chart_data.json` preserves the source headers and rows, including redundant display columns. `build_data.mjs` reproduces the CSVs from this snapshot with Node.js and no external packages. Cite Carnegie as the original study and describe the extraction and calculations in your app.

## Files

| File | Rows | Role |
|---|---:|---|
| ai_talent_country_summary.csv | 11 | Recommended main Streamlit dataset: joins the two country/region tables and computes retained and destination counts. |
| published_retention.csv | 11 | Published undergraduate education totals and retention percentages, with numeric formatting cleaned. |
| published_mobility.csv | 11 | Published outside-origin and incoming counts; net difference is calculated as arrivals minus departures. |
| selected_career_paths.csv | 18 | Published combinations of undergraduate, graduate and work geography. A selected subset, not a complete flow matrix. |
| published_chart_data.json | 3 tables | Preserved public chart data, titles, headers, URLs and retrieval metadata. |
| build_data.mjs | — | Reproducible CSV transformation and consistency checks. |

## Scope: read before plotting

- The study uses authors of accepted NeurIPS papers. This package covers its 2025 conference cohort with complete three-stage histories: 10,280 researchers, about 40% of the cohort's unique authors. It does not cover all AI researchers or all people working in AI.
- The conference cohort is 2025; the employment observation year is 2026. Do not label these as 2025 employment observations. Undergraduate study occurred in different earlier years; these are not annual graduate counts.
- The complete-history subset is non-random. Researchers without complete profiles are excluded. Findings describe the observed sample and should not be presented as population estimates without qualification.
- For the main retention measure, 'training' means undergraduate institution country. It is not nationality, citizenship, birthplace, or necessarily the country of an AI-specific degree. Graduate education appears only in the selected career-path table.
- Employment geography follows the study's institution/employer country assignments. For multinational employers, that may reflect headquarters/home country rather than the researcher's physical office. These are education-to-employment affiliation comparisons, not verified immigration events.
- 'Retained' means undergraduate and employment geography match at observation. It may include researchers who left and later returned; it does not prove uninterrupted residence.
- Europe and Other are grouped geographies, not individual countries. The study treats the UK separately from Europe and groups Hong Kong with China. Matching within Europe or Other does not demonstrate retention within the same individual country. Do not put those grouped labels on a country choropleth without an explicit treatment.
- The 18 selected career paths total 8,214 researchers (79.9027% of 10,280). The other 2,066 researchers' detailed paths are not provided here. Do not infer missing flows as zeros, calculate full-sample retention from these 18 paths, or label their Sankey as all researchers.
- This package is a single-cohort snapshot. Do not invent annual trends or attribute patterns causally to government policies. A separate comparable source would be needed for trend analysis.

## Main CSV column definitions

Counts are people in the observed cohort. Percent columns use the 0–100 scale.

| Column | Meaning / derivation |
|---|---|
| conference_cohort_year | 2025: accepted-paper cohort. |
| workplace_observation_year | 2026: employment observation year. |
| country_or_region | Published geography label. |
| geography_type | country or grouped_region; Europe and Other are grouped_region. |
| undergraduate_educated_count | Published 'Own graduates' count: cohort researchers educated in that geography at undergraduate level. |
| working_outside_origin_group_count | Published 'Left' count: undergraduate geography differs from work geography. |
| same_origin_work_group_count | undergraduate_educated_count minus working_outside_origin_group_count. |
| educated_elsewhere_working_here_count | Published 'Arrived' count: researchers working here whose undergraduate geography is elsewhere. |
| work_destination_count | same_origin_work_group_count plus educated_elsewhere_working_here_count. |
| net_difference_count | educated_elsewhere_working_here_count minus working_outside_origin_group_count. This also equals work_destination_count minus undergraduate_educated_count. |
| published_retention_percent | Publisher's retention percentage, rounded to one decimal place. |
| recalculated_retention_percent | same_origin_work_group_count / undergraduate_educated_count × 100, saved to six decimal places. Extra digits are arithmetic, not greater measurement certainty. |
| retention_source_url | Public source for the education total and published retention percentage. |
| mobility_source_url | Public source for incoming/outgoing counts. |

## Checks completed

1. Eleven unique country/region groups join without unmatched rows.
2. Undergraduate education totals sum to 10,280.
3. Derived work-destination totals also sum to 10,280.
4. Net differences sum to zero across all groups.
5. Every recalculated retention percentage matches the published rate when rounded to one decimal place.
6. The selected career-path table contains 18 rows and sums to 8,214, below the full cohort total.

### Example for the individual recording

Select USA in the app. The source retention table reports 1,369 researchers with undergraduate education in the USA. The mobility table reports 155 with work geography elsewhere. Therefore 1,369 − 155 = 1,214 have matching undergraduate and employment geography. The rate is 1,214 / 1,369 × 100 = 88.677867%, or 88.7% at the publisher's precision. Show both source rows and this calculation on screen.

## Suitable app components

- Grouped bars comparing undergraduate education counts and work-destination counts.
- Ranked retention bars with the undergraduate denominator visible.
- Net difference bars and filters for country/region.
- Work-destination shares calculated against the complete 10,280-person cohort.
- An explicitly labelled selected-career-paths view using the 18 published paths.

For a retention chart comparing individual countries, exclude Europe and Other or place them in a clearly separated grouped-region view. The data provides evidence relevant to talent policy; it does not tell an analyst which policy caused a pattern or would change it.
