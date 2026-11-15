from flask import Flask, render_template, request, jsonify, make_response
import requests
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime

app = Flask(__name__)
NASA_URL = "https://power.larc.nasa.gov/api/temporal/monthly/point"
PARAMETERS = {
    "temperature": {"code": "T2M", "label": "2 m Air Temperature", "unit": "°C", "aggregation": "annual mean"},
    "precipitation": {"code": "PRECTOTCORR", "label": "Corrected Precipitation", "unit": "mm/day", "aggregation": "annual mean of monthly mean daily rates"},
    "humidity": {"code": "RH2M", "label": "Relative Humidity at 2 m", "unit": "%", "aggregation": "annual mean"},
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/analyze")
def analyze():
    try:
        lat = float(request.args.get("lat", "9.9312"))
        lon = float(request.args.get("lon", "76.2673"))
        variable = request.args.get("variable", "temperature")
        start = int(request.args.get("start", "2001"))
        end = int(request.args.get("end", "2025"))
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return jsonify({"error": "Latitude must be -90 to 90 and longitude -180 to 180."}), 400
        if variable not in PARAMETERS:
            return jsonify({"error": "Unsupported variable."}), 400
        if start < 1981 or end > datetime.now().year - 1 or start >= end or end - start < 9:
            return jsonify({"error": "Choose a period of at least 10 years, starting from 1981 and ending no later than the previous complete year."}), 400

        meta = PARAMETERS[variable]
        params = {
            "parameters": meta["code"], "community": "AG" if variable == "precipitation" else "SB",
            "longitude": lon, "latitude": lat, "start": start, "end": end, "format": "JSON"
        }
        response = requests.get(NASA_URL, params=params, timeout=45)
        response.raise_for_status()
        payload = response.json()
        values = payload.get("properties", {}).get("parameter", {}).get(meta["code"])
        if not values:
            return jsonify({"error": "NASA POWER returned no data for this request. Try another coordinate or date range."}), 502

        rows = []
        for yyyymm, value in values.items():
            try:
                val = float(value)
                if val > -900:
                    rows.append({"date": pd.to_datetime(yyyymm, format="%Y%m"), "value": val})
            except (ValueError, TypeError):
                continue
        df = pd.DataFrame(rows)
        if df.empty:
            return jsonify({"error": "No valid observations were returned by NASA POWER."}), 502
        df["year"] = df["date"].dt.year
        annual = df.groupby("year")["value"].mean().reset_index()
        annual = annual.dropna()
        if len(annual) < 8:
            return jsonify({"error": "Not enough valid annual observations for a reliable trend test."}), 502

        x = annual["year"].to_numpy(dtype=float)
        y = annual["value"].to_numpy(dtype=float)
        lr = stats.linregress(x, y)
        tau, p_value = stats.kendalltau(x, y, nan_policy="omit")
        # Sen's slope: median of all pairwise slopes, robust to outliers.
        sen_slopes = [(y[j] - y[i]) / (x[j] - x[i]) for i in range(len(x)) for j in range(i + 1, len(x))]
        sen_slope = float(np.median(sen_slopes))
        ci_low = float(lr.slope - 1.96 * lr.stderr) if np.isfinite(lr.stderr) else None
        ci_high = float(lr.slope + 1.96 * lr.stderr) if np.isfinite(lr.stderr) else None
        significant = bool(p_value < 0.05)
        direction = "increasing" if sen_slope > 0 else "decreasing" if sen_slope < 0 else "approximately stable"
        if significant:
            interpretation = f"The annual series shows a statistically significant {direction} monotonic association over this period (Mann–Kendall/Kendall test p = {p_value:.4f}). This describes the selected coordinate and dataset; it does not by itself establish a cause."
        else:
            interpretation = f"The analysis does not find statistically significant evidence of a monotonic trend at the 0.05 level (p = {p_value:.4f}). The estimated direction is {direction}, but the evidence is insufficient to call it a statistically significant trend."

        return jsonify({
            "source": "NASA POWER Monthly API", "source_url": "https://power.larc.nasa.gov/docs/services/api/temporal/monthly/",
            "parameter": meta["code"], "variable": meta["label"], "unit": meta["unit"],
            "latitude": lat, "longitude": lon, "start": int(x.min()), "end": int(x.max()),
            "aggregation": meta["aggregation"], "years": x.astype(int).tolist(),
            "values": np.round(y, 3).tolist(), "trend_line": np.round(lr.intercept + lr.slope*x, 3).tolist(),
            "sen_slope_per_year": round(sen_slope, 5), "linear_slope_per_year": round(float(lr.slope), 5),
            "slope_ci_approx_95": [round(ci_low, 5), round(ci_high, 5)] if ci_low is not None else None,
            "kendall_tau": round(float(tau), 4), "p_value": round(float(p_value), 6),
            "significant_at_005": significant, "direction": direction,
            "n_years": len(annual), "interpretation": interpretation,
            "caveat": "NASA POWER point data are not a state-wide spatial average. Monthly values are aggregated to annual means here; seasonality and autocorrelation can affect inference. The displayed slope interval is an approximate ordinary-least-squares interval, not a Sen-slope confidence interval."
        })
    except requests.RequestException as exc:
        return jsonify({"error": f"Could not reach NASA POWER right now: {exc}. Please retry."}), 502
    except Exception as exc:
        app.logger.exception("Analysis failed")
        return jsonify({"error": f"Analysis failed: {str(exc)}"}), 500

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "app": "STRANGER"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
