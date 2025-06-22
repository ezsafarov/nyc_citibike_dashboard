import streamlit as st
from streamlit.components.v1 import html


# Page config
st.set_page_config(page_title="Citibike Dashboard – Strategic Expansion Analysis (2022)", layout="wide")

# Title and description
st.title("Citibike Dashboard – Strategic Expansion Analysis (2022)")
st.markdown("""

This dashboard explores patterns in bike usage, user behavior, and weather across New York City's Citibike system in 2022.

It is designed to:

- Understand trip behavior and seasonal trends
- Identify the busiest start stations
- Compare usage patterns between member and casual riders
- Visualize city-wide bike usage patterns using an interactive map

By combining trip and weather data, the dashboard supports data-driven decisions around station expansion, service optimization, and user engagement strategies.

""")

#1

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Load and prepare data
df = pd.read_csv("/Users/emilsafarov/Library/CloudStorage/OneDrive-Personal/CF/CF_S2/nyc_citibike_dashboard_old/Data/Output/citibike_weather_merged_2022.csv")

df['value'] = 1
station_counts = df.groupby('start_station_name')['value'].count().reset_index()
top20 = station_counts.nlargest(20, 'value')

# Create the bar chart
fig = go.Figure(go.Bar(
    x=top20['value'],
    y=top20['start_station_name'],
    orientation='h',
    marker=dict(color=top20['value'], colorscale='Blues')
))

fig.update_layout(
    title='The majority of trips begin in Jersey City and Hoboken, indicating these areas are key hubs for Citibike usage.',
    xaxis_title='Number of Rides',
    yaxis_title='Start Station',
    height=800,
    width=1000,
    font=dict(size=26),  # Increased from 14 → 18 (~+25%)
    yaxis=dict(
        autorange='reversed',
        tickfont=dict(size=13)  # Increased from 10 → 13
    ),
    xaxis=dict(
        tickfont=dict(size=13)  # Increased from 10 → 13
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=180)
)


# Display in Streamlit
st.subheader("Top 20 Most Frequent Start Stations")
st.plotly_chart(fig, use_container_width=True)


# 2

from plotly.subplots import make_subplots
import plotly.graph_objects as go

# --- Daily trip aggregation ---
daily_trips = df.groupby("date")["ride_id"].count().reset_index(name="trip_count")
daily_temp = df.groupby("date")["avg_temp"].mean().reset_index()
df_daily = pd.merge(daily_trips, daily_temp, on="date")

# --- Create dual-axis line chart ---
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

# Line 1: Daily bike trips (right axis)
fig2.add_trace(
    go.Scatter(
        x=df_daily["date"],
        y=df_daily["trip_count"],
        name="Daily Bike Trips",
        line=dict(color="red", width=2)
    ),
    secondary_y=True
)

# Line 2: Avg temperature (left axis)
fig2.add_trace(
    go.Scatter(
        x=df_daily["date"],
        y=df_daily["avg_temp"],
        name="Avg Temperature (°C)",
        line=dict(color="blue", width=2)
    ),
    secondary_y=False
)

# Layout setup
fig2.update_layout(
    title="Daily Bike Trip Count vs. Temperature (2022)",
    xaxis_title="Date",
    height=600,
    font=dict(size=14),
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend=dict(orientation="h", y=-0.2)
)

fig2.update_yaxes(title_text="Avg Temperature (°C)", secondary_y=False)
fig2.update_yaxes(title_text="Trip Count", secondary_y=True)

# Display in Streamlit
st.subheader("Daily Bike Trips vs. Average Temperature")
st.plotly_chart(fig2, use_container_width=True)


#3

import plotly.express as px
import plotly.graph_objects as go

# --- Count rideable types ---
rideable_counts = df["rideable_type"].value_counts().reset_index()
rideable_counts.columns = ["rideable_type", "count"]

# --- Count user types ---
user_counts = df["member_casual"].value_counts().reset_index()
user_counts.columns = ["member_casual", "count"]

# --- Streamlit layout: two columns side by side ---
col1, col2 = st.columns(2)

# --- Left column: Bar chart for rideable types ---
with col1:
    st.subheader("Rideable Type Distribution")
    fig_bar = px.bar(
        rideable_counts,
        x="rideable_type",
        y="count",
        color="rideable_type",
        color_discrete_sequence=["#1f3c88", "#3d5a80", "#98c1d9"],
        labels={"rideable_type": "Bike Type", "count": "Count"}
    )
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Right column: Pie chart for user roles ---
with col2:
    st.subheader("User Type (Member vs Casual)")
    fig_pie = go.Figure(
        data=[go.Pie(
            labels=user_counts["member_casual"],
            values=user_counts["count"],
            marker=dict(colors=["#a8dadc", "#e63946"]),
            hole=0.3,
            textinfo="percent+label"
        )]
    )
    fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_pie, use_container_width=True)



#4


from streamlit.components.v1 import html

# --- Kepler.gl Map Section ---
st.subheader("Aggregated Bike Trips in NYC")

map_path = "/Users/emilsafarov/Library/CloudStorage/OneDrive-Personal/CF/CF_S2/nyc_citibike_dashboard/Scripts/nyc_bike_map_v2.html"

with open(map_path, 'r') as f:
    map_html = f.read()

html(map_html, height=800)


