import streamlit as st
import pandas as pd

# Set page layout and title
st.set_page_config(page_title="Hospital Bed Capacity Dashboard", layout="wide", page_icon="🏥")

# App Header
st.title("🏥 Hospital Bed Capacity Dashboard")
st.markdown("Monitor real-time bed availability and occupancy rates across critical wards.")
st.markdown("---")

# 1. Create Dummy Data
@st.cache_data
def load_dummy_data():
    data = {
        "Ward": ["ICU", "General", "Maternity"],
        "Total Beds": [50, 150, 80],
        "Occupied Beds": [42, 115, 35]
    }
    df = pd.DataFrame(data)
    # Calculate extra metrics
    df["Available Beds"] = df["Total Beds"] - df["Occupied Beds"]
    df["Occupancy Rate (%)"] = ((df["Occupied Beds"] / df["Total Beds"]) * 100).round(1)
    return df

df = load_dummy_data()

# 3. Sidebar Filter Slider
st.sidebar.header("Dashboard Filters")
min_occupancy = st.sidebar.slider(
    "Filter by Minimum Occupancy Rate (%)",
    min_value=0,
    max_value=100,
    value=40,
    step=5
)

# Filter the dataframe based on slider input
filtered_df = df[df["Occupancy Rate (%)"] >= min_occupancy]

# High-level KPIs (Key Performance Indicators)
total_beds = df["Total Beds"].sum()
total_occupied = df["Occupied Beds"].sum()
overall_occupancy = round((total_occupied / total_beds) * 100, 1)

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="Total Hospital Beds", value=total_beds)
kpi2.metric(label="Total Occupied Beds", value=total_occupied)
kpi3.metric(label="Overall Occupancy Rate", value=f"{overall_occupancy}%")

st.markdown("---")

# Main Content Layout
if not filtered_df.empty:
    col1, col2 = st.columns([4, 5])

    with col1:
        st.subheader("📋 Ward Statistics")
        # Display the filtered dataframe cleanly
        st.dataframe(
            filtered_df[["Ward", "Total Beds", "Occupied Beds", "Available Beds", "Occupancy Rate (%)"]],
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.subheader("📊 Bed Occupancy Visualization")
        # 2. Display a Bar Chart of Occupancy
        # Setting 'Ward' as index allows Streamlit to automatically use it for the X-axis labels
        chart_data = filtered_df.set_index("Ward")[["Occupied Beds", "Total Beds"]]
        st.bar_chart(chart_data, color=["#ff4b4b", "#0068c9"])
        st.caption("🔴 Occupied Beds  |  🔵 Total Beds Capacity")

else:
    st.warning("No wards meet the selected minimum occupancy rate filter. Try lowering the slider values in the sidebar.")
