# AI Provenance

The AI provenance matrix: a row per substantive AI use (artefact, who, tool, what was asked, what came back, how it was verified, outcome). Each member owns at least one row. The verification must name a check that could have failed.

Remove these instructions before submitting.
---

- Artefact: Stacked Bar Chart
- Group Member: Edwin Lansangan
- AI Tool: Google Gemini
- AI Question/Instruction: Implement a stacked bar chart showing workforce composition in Streamlit
- AI Response: python code for a stacked bar chart in streamlit
- Verification: The resulting code was tested locally for functionality. The totals for imported talent and homegrown talent were verified one by one. This is to make sure that the code was able to read the data correctly as the data reading step could sometimes fail.
- Outcome: The totals were read correctly and the code was subsequently used with some modifications on axis titles and colour schemes.
---

- Artefact: Bubble Chart
- Group Member: Kiemas Zaidan
- AI Tool: Claude
- AI Question/Instruction: Checking for colour consistency on the previously made code to apply on this dashboard.
- AI Response: looks good.
- Verification: tested locally, works fine.
- Outcome: the colour scheme checks out.
---
 
- Artefact: Diverging and Grouped Bar Charts
- Group Member: Hasnain Abbas
- AI Tool: ChatGPT
- AI Question/Instruction: Enhance the existing Train vs Work visualisation in Streamlit by country highlighting and filters.
- AI Response: Python code for a enhanced diverging bar chart and group bar chart showing net differences through new color filters and highlighting.
- Verification: Both charts were tested locally in Streamlit to check their functionality and whether switching between them worked correctly. The USA (+2,145) and China (−1,729) net differences were also checked against the dataset to confirm the calculations.
- Outcome: Both visualisations displayed correctly, and the interactive features worked as expected. The enhanced code was used in the final Train vs Work tab.
---

- Artefact: Donut chart ("Where do researchers from (or in) a country end up?")
- Group Member: Idhika Vaidya
- AI Tool: Claude
- AI Question/Instruction: Asked Claude to build a chart showing where researchers trained in a country now work, and where a country's workforce trained, using the career-path data. Tried a Sankey diagram first to show directional movement, then a pie chart, then a donut chart.
- AI Response: Streamlit/Plotly code for each version. The Sankey showed direction of movement but was too cluttered, with too many origin–graduate–work combinations to read. The pie was easier to read but less clean than the donut. The donut chart with a country selector showed the breakdown most clearly and has room for the total in the centre.
- Verification: Ran the app locally and selected China. Checked that the slices add up to the 5,903 in the centre, that "Stayed" (4,056) and total leavers (1,847) match ai_talent_country_summary.csv, and that the named destinations (USA 1,179, Singapore 147, Europe 80) match selected_career_paths.csv. The grey "destination not published" slice should equal 1,847 minus the named destinations, which is 441. This could have failed if the code counted China→USA→China rows (132 returners) as leavers, or if the slices did not sum to the cohort total. Repeated the sum check for USA and India.
- Outcome: Kept the donut chart. The slices summed correctly, and unpublished destinations stay as one grey slice instead of being spread across countries. Dropped the Sankey (too cluttered) and the pie (less clean than the donut).
