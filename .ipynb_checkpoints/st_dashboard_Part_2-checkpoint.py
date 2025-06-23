# 0 menu

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  
from streamlit.components.v1 import html

# Page configuration
st.set_page_config(
    page_title="Citibike Dashboard – Strategic Expansion Analysis",
    layout="wide"
)

# Load data
df = pd.read_csv("bike_sample.csv")

# Sidebar navigation
st.sidebar.title("NYC CitiBike Dashboard")
page = st.sidebar.selectbox("Choose a page", [
    "Intro",
    "Trip Count & Temperature Relationship",
    "Bike Type and User Role Breakdown",  
    "Top Start Stations",
    "Interactive Map",
    "Core Operational Questions"
])


# 1 introduction page + photo

if page == "Intro":
    # Main heading
    st.header("Citibike Dashboard Overview")

    # Subheading for insight/message
    st.subheader("Exploring user behavior, trip volume, and geographic patterns to support strategic system growth.")

    # Introduction description
    st.markdown("""
    This dashboard explores patterns in bike usage, user behavior, and weather across New York City's Citibike system in 2022.

    It is designed to:

    - Understand trip behavior and seasonal trends  
    - Identify the busiest start stations  
    - Compare usage patterns between member and casual riders  
    - Visualize city-wide bike usage patterns using an interactive map  
    """)

    # Intro image
    st.image(
        "Citi_Bike_image.jpg.webp",
        caption="Source: Citi Bike NYC Trip Data (2022) and NOAA Weather Data (2022)",
        use_column_width=True
    )

    # Horizontal line
    st.markdown("---")

    # Author info
    st.markdown("""
    <div style='text-align: center; font-size: 18px;'>
        👤 <strong>Emil Safarov</strong> — Data Analyst &nbsp;|&nbsp; 
        📧 <a href='mailto:e.z.safarov@gmail.com'>Email</a> &nbsp;|&nbsp; 
        🔗 <a href='https://www.linkedin.com/in/emil-safarov-16b520103'>LinkedIn</a> &nbsp;|&nbsp; 
        💻 <a href='https://github.com/ezsafarov'>GitHub</a>
    </div>
    """, unsafe_allow_html=True)


elif page == "Trip Count & Temperature Relationship":
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    # --- Page title and insight ---
    st.header("Trip Count & Temperature Trends")
    st.subheader("Seasonal weather patterns closely align with ridership — warmer months show strong demand growth.")

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
        title="",
        xaxis_title="Date",
        height=600,
        font=dict(size=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(orientation="h", y=-0.2)
    )

    fig2.update_yaxes(title_text="Avg Temperature (°C)", secondary_y=False)
    fig2.update_yaxes(title_text="Trip Count", secondary_y=True)

    # --- Display chart
    st.plotly_chart(fig2, use_container_width=True)

    # --- Dashboard Highlights ---
    st.markdown("""
    ### Dashboard Highlights: Trip Count & Temperature
    - Trip volume rises sharply from April, peaking between June and September during the warmest months  
    - Ridership declines starting in October, with the lowest activity from November to March  
    - Sudden dips may be caused by weather events, holidays, or service disruptions — potential flags for further investigation  
    - These seasonal trends support smarter bike supply, staffing, and maintenance planning, especially ahead of peak months
    """)



# 3 additional bar + pie charts 

elif page == "Bike Type and User Role Breakdown":
    # Consistent page heading and insight
    st.header("Bike Type & User Role Breakdown")
    st.subheader("Dockless bikes dominate system usage, and with members comprising most riders, user insights guide smarter operations.")

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

    # --- Left column: Bar chart for bike types ---
    with col1:
        st.subheader("Bike Type Distribution")
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

    # --- Right column: Pie chart for user types ---
    with col2:
        st.subheader("User Type Split")
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

    # --- Dashboard Highlights
    st.markdown("""
    ### Dashboard Highlights: Bike Type & User Role

    - Dockless bikes (classic and electric) account for nearly all trips, while docked bikes are rarely used  
    - About two-thirds of users are members, reflecting strong commuter-based demand  
    - Casual riders still represent over one-third—often tourists or occasional users  
    - These trends support better fleet planning, targeted engagement, and role-specific service strategies
    """)


# 4 bar chart 

elif page == "Top Start Stations":
    # Page title and key insight
    st.header("Top Start Stations")
    st.subheader("Jersey City and Hoboken emerge as key origin hubs, highlighting infrastructure demand at high-flow locations.")

    # Prepare the data
    df["value"] = 1  # Add helper column
    station_counts = df.groupby("start_station_name")["value"].count().reset_index()
    top20 = station_counts.nlargest(20, "value")

    # Create horizontal bar chart
    fig = go.Figure(go.Bar(
        x=top20["value"],
        y=top20["start_station_name"],
        orientation="h",
        marker=dict(color=top20["value"], colorscale="Blues")
    ))

    fig.update_layout(
        title="",
        xaxis_title="Number of Rides",
        yaxis_title="Start Station",
        height=800,
        font=dict(size=26),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(size=13)
        ),
        xaxis=dict(
            tickfont=dict(size=13)
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=180)
    )

    # Display chart
    st.plotly_chart(fig, use_container_width=True)

    # Add highlights
    st.markdown("""
    ### 🔍 Dashboard Highlights: Top Start Stations

    - Jersey City and Hoboken dominate the top 20 start locations  
    - Key stations like Grove St PATH and Hoboken Terminals record the highest trip volumes  
    - These stations likely serve major commuter flows, dense housing areas, and transit connections  
    - High-demand hubs may require expanded docking capacity, improved inventory planning, and local infrastructure support
    """)



# 5 map

elif page == "Interactive Map":
    st.header("Mapping City's Bike Activity")

    # Path to your exported HTML map
    map_path = "/Users/emilsafarov/Library/CloudStorage/OneDrive-Personal/CF/CF_S2/nyc_citibike_dashboard/nyc_bike_map_v2.html"

    try:
        with open(map_path, "r") as f:
            map_html = f.read()

        # Render map in Streamlit
        html(map_html, height=800)

    except FileNotFoundError:
        st.error(f"Map file not found at: `{map_path}`. Please double-check the path.")


# 6 
elif page == "Core Operational Questions":
    st.header("Dashboard Highlights: Addressing Key Operational Questions")

    st.markdown("""
    ### 1. How much could bike availability be adjusted between November and April?
    - Ridership drops by **30–50%** during colder months.
    - Scale back bike supply by **30–40%** from November to April.
    - Use **per-station historical usage trends** to guide targeted reductions.
    - Maintain **full capacity** at high-demand commuter hubs like **Grove St PATH**.

    ---

    ### 2. How can the need for additional stations along the water be assessed?
    - **Kepler.gl maps** show high origin activity along the Hoboken waterfront.
    - **Buffer analysis** reveals gaps in coverage, especially **west of Stevens Institute of Technology**.
    - Add **2–3 new stations** in inland Hoboken to support unmet demand.
    - Ensure new stations align with **trip patterns** and **planned developments**.

    ---

    ### 3. What strategies support consistent bike availability at popular stations?
    - Apply **predictive analytics** based on hourly usage and weather data.
    - Trigger **automated rebalancing** when bike count falls below thresholds (e.g., <5 bikes).
    - Use **app-based incentives** to encourage returns to underutilized docks.
    - Install **IoT sensors** for real-time station monitoring at key hubs like **Grove St PATH** and **Hoboken Terminal**.
    """)


    # Horizontal line
    st.markdown("---")

    
    st.markdown("""
    <div style='text-align: center; font-size: 18px;'>
        <strong>Emil Safarov</strong> — Data Analyst &nbsp;|&nbsp; 
        <a href='mailto:e.z.safarov@gmail.com'>Email</a> &nbsp;|&nbsp; 
        <a href='https://www.linkedin.com/in/emil-safarov-16b520103'>LinkedIn</a> &nbsp;|&nbsp; 
        <a href='https://github.com/ezsafarov'>GitHub</a>
    </div>
    """, unsafe_allow_html=True)

