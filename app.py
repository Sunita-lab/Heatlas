import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Heatlas", layout="wide")

st.title("🌡️ Heatlas")
st.caption("Urban Heat Intelligence System — Bhubaneswar")

# Data load
df = pd.read_csv("data/samples/final_data.csv")
forecast_df = pd.read_csv("outputs/forecast_7day.csv")
coords_df = pd.read_csv("data/samples/bhubaneswar_coords.csv")
coords_df["ID"] = coords_df["ID"].str.replace("_", "")

# Risk labels
def get_label(score):
    if score >= 0.80: return "High"
    elif score >= 0.73: return "Medium"
    else: return "Low"

df["risk_label"] = df["risk_score"].apply(get_label)
color_map = {"High": "red", "Medium": "orange", "Low": "green"}

# Merge coordinates
map_df = df.merge(coords_df[["ID", "Latitude", "Longitude"]], on="ID")

# --- MAP ---
st.subheader("Heat Risk Map")
m = folium.Map(location=[20.3, 85.82], zoom_start=12)

for _, row in map_df.iterrows():
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=10,
        color=color_map[row["risk_label"]],
        fill=True,
        fill_opacity=0.8,
        popup=f"{row['ID']}<br>Risk: {row['risk_label']}<br>Score: {row['risk_score']:.3f}"
    ).add_to(m)

st_folium(m, width=900, height=500)

# --- NEIGHBORHOOD DETAIL ---
st.subheader("Neighborhood Detail")
selected = st.selectbox("Select Neighborhood", df["ID"].sort_values())

row = df[df["ID"] == selected].iloc[0]
col1, col2, col3, col4 = st.columns(4)
col1.metric("Risk Score", round(row["risk_score"], 3))
col2.metric("Temperature", f"{row['temperature']}°C")
col3.metric("NDVI", round(row["ndvi"], 3))
col4.metric("Population Density", round(row["population_density"], 1))

# --- 7 DAY FORECAST ---
st.subheader(f"7-Day Risk Forecast — {selected}")

hood_forecast = forecast_df[forecast_df["neighborhood"] == selected].sort_values("date")

if not hood_forecast.empty:
    st.line_chart(hood_forecast.set_index("date")["risk_score"])
else:
    st.info("Forecast data not available for this neighborhood.")