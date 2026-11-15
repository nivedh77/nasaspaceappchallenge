# NASA Space Apps 2026 — Submission draft

## Project name
STRANGER — Earth System Intelligence & Trend Detection

## Project summary (edit to match the actual finished build)
STRANGER is an interactive Earth-system investigation prototype that helps users explore how environmental variables change over time at a selected location. It retrieves monthly temperature, precipitation, and relative-humidity observations from NASA POWER, aggregates valid observations into annual means, and visualizes the resulting time series. To move beyond a simple chart, STRANGER calculates a robust Theil–Sen slope and Kendall rank-correlation statistic with a p-value, then explains whether the evidence meets a conventional 0.05 significance threshold. Users can inspect the selected coordinates, date range, data source, and methodological limitations, and export the time series and an investigation report. STRANGER is designed as an accessible starting point for data literacy and Earth-science exploration; it does not infer causation or treat a single coordinate as a regional average.

## Project demonstration
Create a screen recording of no more than 30 seconds showing: (1) choose Kochi, (2) select temperature and run analysis, (3) show the real NASA POWER response and chart, (4) point to Sen's slope and p-value, (5) export the CSV/report. Only record this after verifying the live deployed app.

## Project link
[PASTE PUBLIC DEPLOYED URL — must work without login]

## Project demonstration link
[PASTE PUBLIC VIDEO URL — max 30 seconds]

## Project details
STRANGER is implemented as a Flask web application with an HTML/CSS/JavaScript interface and Chart.js visualization. The backend requests monthly point data from NASA POWER's Temporal Monthly API using the selected latitude, longitude, parameter, and year range. It processes the returned JSON into annual means and performs two complementary trend summaries: Theil–Sen's median pairwise slope estimates the rate and direction of change, while Kendall's rank correlation test provides tau and a p-value. A p-value below 0.05 is labelled statistically significant under the chosen test, while the interface explicitly warns that statistical association is not causation. The interface exposes the NASA parameter code, source documentation, coordinates, aggregation approach, and limitations. Users can download the annual time series as CSV and save a text report. The initial demonstration uses a point in Kochi, Kerala; it must not be described as a state-wide average. Future work could add spatially averaged regional datasets, explicit seasonal adjustment, autocorrelation-aware significance tests, and cross-region comparisons.

## Use of Super Intelligence
Declare the actual tools used. If ChatGPT or another AI assistant helped generate or edit code, text, design, or imagery, disclose those categories in the official form. Do not select "I did not use SI" if AI tools were used. No AI-generated images are included in this prototype.

## NASA Data
Link Text: NASA POWER Monthly and Annual API
Link URL: https://power.larc.nasa.gov/docs/services/api/temporal/monthly/

Link Text: NASA POWER API Overview
Link URL: https://power.larc.nasa.gov/docs/services/api/

## Space Agency Partner & Other Data
Link Text: Chart.js
Link URL: https://www.chartjs.org/docs/latest/

Link Text: SciPy Statistics
Link URL: https://docs.scipy.org/doc/scipy/reference/stats.html

Link Text: Pandas documentation
Link URL: https://pandas.pydata.org/docs/

## Important before submission
Replace both placeholder links. Test the deployed URL on a device where you are not logged in. Ensure the demo is 30 seconds or less. Confirm that the live app successfully retrieves NASA POWER data. Report actual AI usage honestly. Do not claim features that are not present in the deployed version.
