# STRANGER — Earth System Intelligence & Trend Detection

An educational prototype for exploring long-term Earth-system signals using NASA POWER monthly point data.

## What it does
- Requests monthly NASA POWER data for a user-selected coordinate and year range.
- Aggregates valid monthly values into annual means.
- Calculates Theil–Sen median pairwise slope and Kendall rank correlation / p-value.
- Displays annual observations and a linear-fit visual guide.
- Exports a CSV time series and a plain-text investigation report.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## Data source
NASA POWER Monthly API: https://power.larc.nasa.gov/docs/services/api/temporal/monthly/

The app uses `T2M` (2 m air temperature), `PRECTOTCORR` (corrected precipitation), and `RH2M` (relative humidity at 2 m). POWER meteorological parameters are derived from the MERRA-2 assimilation model. They are not direct satellite pixel observations. Precipitation is displayed as the annual mean of monthly mean daily rates (mm/day), not annual accumulated rainfall.

## Statistical method and limitations
Annual means are calculated from available monthly values. Sen's slope is the median of all pairwise annual slopes. Kendall's tau and its p-value are calculated using SciPy's Kendall correlation implementation. The app uses p < 0.05 as a conventional threshold, not proof of causation. The linear regression slope interval is approximate and is not a confidence interval for Sen's slope. Serial correlation, missing months, seasonality, spatial representativeness, and data product uncertainty can affect interpretation. A point coordinate is not a state-wide spatial average.

## Deployment (Render)
1. Push this folder to a GitHub repository.
2. Create a new Web Service on Render and connect the repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Wait for deployment, then test `/api/health` and run an analysis in the browser.

## Project status
This is a hackathon prototype, not an official NASA product. Verify live API responses and calculations before presenting results. Do not claim that NASA endorses STRANGER.
