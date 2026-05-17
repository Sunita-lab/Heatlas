import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Heatlas", layout="wide", page_icon="🌡️")

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

/* Base */
html, body, [class*="css"] {
    background-color: #0d0d0d;
    color: #e8e0d0;
    font-family: 'DM Sans', sans-serif;
}

/* Hide default streamlit elements */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 2rem; padding-bottom: 2rem;}

/* Title area */
.heatlas-header {
    border-bottom: 1px solid #2a2a2a;
    padding-bottom: 1.2rem;
    margin-bottom: 2rem;
}
.heatlas-title {
    font-family: 'Space Mono', monospace;
    font-size: 3.2rem;
    font-weight: 700;
    color: #ff6b35;
    letter-spacing: -1px;
    margin: 0;
}
.heatlas-subtitle {
    font-size: 0.85rem;
    color: #888;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: #161616;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    padding: 1rem 1.2rem;
}
[data-testid="metric-container"] label {
    color: #666 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ff6b35 !important;
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem !important;
}

/* Risk badge */
.risk-badge {
    display: inline-block;
    padding: 0.3rem 1rem;
    border-radius: 4px;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 1.5rem;
}
.risk-high   { background: #3d1010; color: #ff4444; border: 1px solid #ff4444; }
.risk-medium { background: #2d1f00; color: #ff9500; border: 1px solid #ff9500; }
.risk-low    { background: #0d2d14; color: #22c55e; border: 1px solid #22c55e; }

/* Section headers */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 0.8rem;
    margin-top: 2rem;
}

/* Selectbox */
[data-testid="stSelectbox"] label {
    color: #666;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Summary pills */
.summary-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.summary-pill {
    padding: 0.4rem 1rem;
    border-radius: 4px;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
}
.pill-high   { background: #3d1010; color: #ff4444; }
.pill-medium { background: #2d1f00; color: #ff9500; }
.pill-low    { background: #0d2d14; color: #22c55e; }

/* Divider */
hr { border-color: #1e1e1e; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="heatlas-header">
    <p class="heatlas-title">🌡️ HEATLAS</p>
    <p class="heatlas-subtitle">Urban Heat Intelligence System &nbsp;·&nbsp; Bhubaneswar, India</p>
</div>
""", unsafe_allow_html=True)

# ── Data ───────────────────────────────────────────────────────────────────────
df = pd.read_csv("data/samples/final_data_v2.csv")
forecast_df = pd.read_csv("outputs/forecast_7day.csv")
coords_df = pd.read_csv("data/samples/bhubaneswar_coords.csv")
coords_df["ID"] = coords_df["ID"].str.replace("_", "")

df["risk_label"] = df["risk_label_v2"]
color_map = {"High": "red", "Medium": "orange", "Low": "green"}
map_df = df.merge(coords_df[["ID", "Latitude", "Longitude"]], on="ID")

# ── Summary pills ──────────────────────────────────────────────────────────────
high_n   = (df["risk_label"] == "High").sum()
medium_n = (df["risk_label"] == "Medium").sum()
low_n    = (df["risk_label"] == "Low").sum()

st.markdown(f"""
<div class="summary-row">
    <span class="summary-pill pill-high">● {high_n} High Risk</span>
    <span class="summary-pill pill-medium">● {medium_n} Medium Risk</span>
    <span class="summary-pill pill-low">● {low_n} Low Risk</span>
</div>
""", unsafe_allow_html=True)

# ── Map ────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Heat Risk Map</p>', unsafe_allow_html=True)

m = folium.Map(
    location=[20.3, 85.82],
    zoom_start=12,
    tiles="CartoDB positron"
)

for _, row in map_df.iterrows():
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=10,
        color=color_map[row["risk_label"]],
        fill=True,
        fill_opacity=0.85,
        popup=folium.Popup(
            f"<b style='font-family:monospace'>{row['ID']}</b><br>"
            f"Risk: {row['risk_label']}<br>"
            f"Score: {row['risk_score_v2']:.3f}<br>"
            f"Temp: {row['temperature']}°C<br>"
            f"NDVI: {row['ndvi']:.3f}",
            max_width=180
        )
    ).add_to(m)

st_folium(m, width=None, height=480)

# ── Neighborhood Detail ────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Neighborhood Detail</p>', unsafe_allow_html=True)

selected = st.selectbox("", df["ID"].sort_values(), label_visibility="collapsed")
row = df[df["ID"] == selected].iloc[0]

label = row["risk_label"]
badge_class = f"risk-{label.lower()}"
st.markdown(f'<span class="risk-badge {badge_class}">{label.upper()} RISK</span>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Risk Score", f"{row['risk_score_v2']:.3f}")
col2.metric("Temperature", f"{row['temperature']}°C")
col3.metric("NDVI", f"{row['ndvi']:.3f}")
col4.metric("Pop. Density", f"{row['population_density']:.1f}")

# ── Forecast Chart ─────────────────────────────────────────────────────────────
st.markdown(f'<p class="section-label">7-Day Risk Forecast</p>', unsafe_allow_html=True)

hood_forecast = forecast_df[forecast_df["neighborhood"] == selected].sort_values("date")

if not hood_forecast.empty:
    chart_df = hood_forecast.set_index("date")[["risk_score"]]
    st.line_chart(chart_df, color=["#ff6b35"])
else:
    st.info("Forecast data not available for this neighborhood.")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<hr>
<p style='color:#333; font-size:0.75rem; font-family:monospace; text-align:center; margin-top:1rem;'>
HEATLAS v0.2 &nbsp;·&nbsp; Data: NASA APPEEARS · WorldPop · Open-Meteo &nbsp;·&nbsp; Active Development
</p>
""", unsafe_allow_html=True)