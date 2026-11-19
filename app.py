import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# Page configurations
st.set_page_config(
    page_title="CHRIST University | Event Analytics", page_icon="🎓", layout="wide"
)

# data file path
DATA_FILE = "event_registration.csv"
# Constraints
REQUIRED_COLUMNS = [
    "Event_ID",
    "Event_Name",
    "Category",
    "Department",
    "Academic_Year",
    "Month",
    "Registrations",
    "Attended",
    "Capacity",
]

MONTH_ORDER = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


@st.cache_data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        raise ValueError("The CSV file is empty.")
    except pd.errors.ParserError:
        raise ValueError("The CSV file has an invalid format.")
    # Checking required columns
    missing_columns = set(REQUIRED_COLUMNS) - set(data.columns)
    if missing_columns:
        raise ValueError(
            "Missing required columns: " + ", ".join(sorted(missing_columns))
        )
    # Keep only required columns
    data = data[REQUIRED_COLUMNS].copy()
    if data.empty:
        raise ValueError("The dataset contains no event records.")
    # removing extra spaces if any
    text_columns = [
        "Event_ID",
        "Event_Name",
        "Category",
        "Department",
        "Academic_Year",
        "Month",
    ]
    for column in text_columns:
        data[column] = data[column].astype("string").str.strip()
    # Checking missing and empty values
    if data.isna().any().any():
        raise ValueError("Required fields cannot contain missing values.")
    for column in text_columns:
        if data[column].eq("").any():
            raise ValueError(f"{column} cannot contain empty values.")
    # Check for unique event IDs
    if data["Event_ID"].duplicated().any():
        duplicate_ids = data.loc[data["Event_ID"].duplicated(), "Event_ID"].tolist()
        raise ValueError(f"Duplicate Event_ID values found: {duplicate_ids}")
    # Date Validation Check
    year_pattern = r"^\d{4}-\d{2}$"
    if not data["Academic_Year"].str.match(year_pattern).all():
        raise ValueError(
            "Academic_Year must follow the format YYYY-YY, " "for example 2025-26."
        )
    for year in data["Academic_Year"].unique():
        start_year = int(year[:4])
        end_year = int(year[5:])
        if end_year != (start_year + 1) % 100:
            raise ValueError(f"Invalid academic year sequence: {year}")
    # Month name Validation
    valid_months = set(MONTH_ORDER)
    data["Month"] = data["Month"].str.title()
    invalid_months = set(data["Month"]) - valid_months
    if invalid_months:
        raise ValueError("Invalid month values: " + ", ".join(sorted(invalid_months)))
    # Check for numerical values
    numeric_columns = ["Registrations", "Attended", "Capacity"]
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")
        if data[column].isna().any():
            raise ValueError(f"{column} must contain valid numeric values.")
        if not np.isfinite(data[column]).all():
            raise ValueError(f"{column} cannot contain infinite values.")
        if (data[column] < 0).any():
            raise ValueError(f"{column} cannot contain negative values.")
        if (data[column] % 1 != 0).any():
            raise ValueError(f"{column} must contain whole numbers.")
        data[column] = data[column].astype(int)
    # Validations check attendace not greater than registration numbers
    if (data["Attended"] > data["Registrations"]).any():
        raise ValueError("Attendance cannot exceed registrations.")
    # Validation Check registrations not greater than capacity
    if (data["Registrations"] > data["Capacity"]).any():
        raise ValueError("Registrations cannot exceed event capacity.")
    # Calculating Attendance Rate and Capacity Utilization
    data["Attendance_Rate"] = np.where(
        data["Registrations"] > 0, data["Attended"] / data["Registrations"] * 100, 0
    )
    data["Capacity_Utilization"] = np.where(
        data["Capacity"] > 0, data["Registrations"] / data["Capacity"] * 100, 0
    )
    return data


#  streamlit app layout
st.title("CHRIST University")
st.subheader("Event & Registration Analytics Dashboard")
st.caption(
    "Python CIA3 project."
    "The dataset used in this project is a sample dataset created for demonstration purposes and does not represent real data from CHRIST University."
)
# load the dataset
try:
    df = load_data(DATA_FILE)
except FileNotFoundError:
    st.error("event_registrations.csv was not found")
    st.stop()
except Exception as error:
    st.error(f"Dataset error: {error}")
    st.stop()

# SIDEBAR
st.sidebar.header("Dashboard Filters")

years = ["All"] + sorted(df["Academic_Year"].unique().tolist())
categories = ["All"] + sorted(df["Category"].unique().tolist())
departments = ["All"] + sorted(df["Department"].unique().tolist())

selected_year = st.sidebar.selectbox("Academic Year", years)
selected_category = st.sidebar.selectbox("Event Category", categories)
selected_department = st.sidebar.selectbox("Department", departments)

filtered = df.copy()

if selected_year != "All":
    filtered = filtered[filtered["Academic_Year"] == selected_year]
if selected_category != "All":
    filtered = filtered[filtered["Category"] == selected_category]
if selected_department != "All":
    filtered = filtered[filtered["Department"] == selected_department]

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# MAIN LAYOUT

# Column-wise metrics/cards
total_events = filtered["Event_ID"].nunique()
total_registrations = int(filtered["Registrations"].sum())
total_attended = int(filtered["Attended"].sum())
attendance_rate = (
    total_attended / total_registrations * 100 if total_registrations else 0
)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Event Records", f"{total_events:,}")
k2.metric("Registrations", f"{total_registrations:,}")
k3.metric("Attendance", f"{total_attended:,}")
k4.metric("Attendance Rate", f"{attendance_rate:.1f}%")
