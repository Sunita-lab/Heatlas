# Heatlas
### Urban Heat Intelligence System — Bhubaneswar, India

Heatlas is an AI-assisted urban heat vulnerability analysis system that identifies where heat risk is highest inside a city, why those areas are more vulnerable, and how risk evolves over time.

The project is centered around Bhubaneswar, Odisha — a city where summer heat affects neighborhoods very differently depending on vegetation cover, population density, and surface conditions.

---

## What It Does

- Computes neighborhood-level **heat risk scores** using real environmental data
- Integrates **satellite-derived NDVI** (vegetation health) from NASA APPEEARS
- Extracts **population density** from WorldPop raster data (1km resolution)
- Fetches **live and 7-day forecast weather** via Open-Meteo API
- Clusters neighborhoods into **High / Medium / Low risk zones** using KMeans
- Generates **interactive geospatial maps** of current and forecasted risk

---

## Data Sources

| Data | Source | Method |
|------|--------|--------|
| NDVI (vegetation index) | NASA APPEEARS — MODIS MOD13Q1 | Manual request, 250m resolution |
| Population density | WorldPop `ind_ppp_2020.tif` | Raster extraction via `rasterio` |
| Temperature & Humidity | Open-Meteo API | Live fetch + 7-day forecast |
| Neighborhood coordinates | Manually curated | 20 neighborhoods across Bhubaneswar |

---

## Risk Score Formula

```
Risk Score = (Temperature × 0.4) + (Humidity × 0.2) + (1 - NDVI × 0.2) + (Population Density × 0.2)
```

All parameters are normalized before scoring. Weights reflect the relative contribution of each factor to urban heat vulnerability.

> Note: The current formula is heuristic and manually weighted. Scientific validation and literature-backed weighting are planned for future versions.

---

## Project Structure

```
Heatlas/
│
├── data/
│   └── samples/
│       ├── heatlas-ndvi-MOD13Q1-061-results.csv   # NDVI from NASA APPEEARS
│       ├── population_density.csv                  # Extracted from WorldPop raster
│       └── final_data.csv                          # Merged dataset (all features)
│       ├── bhubaneswar_coords.csv                  # Neighborhood coordinates

├── notebooks/
│   ├── heatlas_main.ipynb                          # Main analysis notebook
│
├── outputs/
│   ├── forecast_7day.csv                           # 7-day risk scores per neighborhood
│   └── forecast_map.html                           # Interactive forecast map
       ├── heatlas_map.html                        # Static risk map
│
└── src/                                            # (in development)
```

---

## Current Capabilities

- 20 Bhubaneswar neighborhoods analyzed
- Real satellite and raster data integrated (not synthetic)
- KMeans clustering for risk zone classification
- 7-day heat risk forecasting per neighborhood
- Interactive Folium maps with popup details

---

## Known Limitations

- Weather API returns low spatial variation across the city — Land Surface Temperature (LST) from satellite thermal data is a planned replacement
- Risk weights are manually defined and not yet scientifically validated
- NDVI and population values are static — temporal tracking not yet implemented
- 20 neighborhoods is a limited sample for a city-wide system

---

## Roadmap

- [ ] Land Surface Temperature (LST) integration
- [ ] Streamlit dashboard for interactive exploration
- [ ] Temporal data storage for trend analysis
- [ ] Literature-backed weight optimization
- [ ] Expanded neighborhood coverage

---

## Tech Stack

`Python` `Pandas` `NumPy` `scikit-learn` `Rasterio` `Folium` `Matplotlib` `Open-Meteo API` `NASA APPEEARS` `WorldPop`

---

## Status

Active development v0.1— ongoing solo project.