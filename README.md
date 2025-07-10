# 🚲 NYC Citibike Dashboard – Strategic Expansion Analysis

This interactive Streamlit dashboard analyzes Citibike trip and weather data from 2022, with a focus on **Jersey City and Hoboken**. It uncovers patterns in ridership, seasonal trends, bike usage types, and station-level demand — helping support smarter fleet scaling, station planning, and user targeting strategies.

---

## 📊 Dashboard Features

- **Trip Volume vs Temperature:**  
  Understand how seasonality impacts ridership patterns.
  
- **Bike Type & User Role Breakdown:**  
  Compare usage by bike type (classic/electric/docked) and user type (member/casual).

- **Top Start Stations:**  
  Explore the busiest start locations to identify operational hotspots.

- **Interactive Geospatial Map (Kepler.gl):**  
  Visualize directional trip flows and locate underserved zones.

- **Core Operational Insights:**  
  Data-driven answers to key strategy questions like:
  - When to scale supply?
  - Where to expand stations?
  - How to keep busy docks stocked?

---

## 🚀 Live Dashboard

👉 [View the Streamlit App](https://your-app-name.streamlit.app)  

---

## 🧠 Summary Recommendations

- Scale back fleet by 30–40% during colder months (Nov–Apr)  
- Add 2–3 new stations west of Stevens Institute in Hoboken  
- Use predictive analytics + IoT monitoring for real-time rebalancing  
- Target casual-heavy zones with localized membership offers

---

## 🗂️ Project Structure

```text
├── Pyfiles/
│   └── st_dashboard_Part_2.py        # Main Streamlit app
├── bike_sample.csv                   # Sample dataset
├── requirements.txt                  # Cleaned dependencies for deployment
├── README.md                         # Project overview
