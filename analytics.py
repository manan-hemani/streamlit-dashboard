from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

DATA_FILE = Path(__file__).parent / "event_registrations.csv"
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
def load_data(file_path: str) -> pd.DataFrame:
    data = pd.read_csv(file_path)

    missing = set(REQUIRED_COLUMNS) - set(data.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
    if data.empty:
        raise ValueError("The dataset contains no records.")

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
        if data[column].isna().any() or data[column].eq("").any():
            raise ValueError(f"{column} contains blank values.")

    if data["Event_ID"].duplicated().any():
        raise ValueError("Event_ID values must be unique.")

    for column in ["Registrations", "Attended", "Capacity"]:
        data[column] = pd.to_numeric(data[column], errors="coerce")
        if data[column].isna().any() or not np.isfinite(data[column]).all():
            raise ValueError(f"{column} must contain valid numeric values.")
        if (data[column] < 0).any() or not np.equal(
            data[column], np.floor(data[column])
        ).all():
            raise ValueError(f"{column} must contain non-negative whole numbers.")
        data[column] = data[column].astype(int)

    if (data["Attended"] > data["Registrations"]).any():
        raise ValueError("Attended cannot exceed Registrations.")
    if (data["Registrations"] > data["Capacity"]).any():
        raise ValueError("Registrations cannot exceed Capacity.")
    if not data["Month"].isin(MONTH_ORDER).all():
        raise ValueError("Month values must be full month names.")

    data["Attendance rate (%)"] = np.where(
        data["Registrations"] > 0,
        data["Attended"] / data["Registrations"] * 100,
        0,
    )
    data["Capacity utilization (%)"] = np.where(
        data["Capacity"] > 0,
        data["Registrations"] / data["Capacity"] * 100,
        0,
    )
    data["Month number"] = data["Month"].map(
        {month: index for index, month in enumerate(MONTH_ORDER, start=1)}
    )
    return data


def get_filtered_data() -> pd.DataFrame:
    try:
        data = load_data(str(DATA_FILE))
    except Exception as error:
        st.error(f"Unable to load the event dataset: {error}")
        st.stop()
    st.sidebar.header("Data filters")
    years = sorted(data["Academic_Year"].unique().tolist())
    departments = sorted(data["Department"].unique().tolist())
    categories = sorted(data["Category"].unique().tolist())

    selected_years = st.sidebar.multiselect(
        "Academic years",
        options=years,
        default=years,
        help="Select one or more academic years to include.",
    )

    # Five category options: pills keep all choices visible at once.
    selected_categories = st.sidebar.pills(
        "Event categories",
        options=categories,
        selection_mode="multi",
        default=categories,
        help="Select one or more event categories.",
    )

    selected_departments = st.sidebar.multiselect(
        "Departments",
        options=departments,
        default=departments,
        help="Select one or more departments.",
    )

    filtered = data[
        data["Academic_Year"].isin(selected_years)
        & data["Category"].isin(selected_categories or [])
        & data["Department"].isin(selected_departments)
    ].copy()
    if filtered.empty:
        st.warning(
            "No records match the selected filters. Adjust the filters in the sidebar."
        )
        st.stop()
    return filtered


def show_page_intro(title: str, description: str, icon: str) -> None:
    st.title(f"{icon} {title}")
    st.write(description)


def show_summary_metrics(data: pd.DataFrame) -> None:
    registrations = int(data["Registrations"].sum())
    attended = int(data["Attended"].sum())
    attendance_rate = attended / registrations * 100 if registrations else 0
    event_count = data["Event_ID"].nunique()

    columns = st.columns(4)
    columns[0].metric("Event records", f"{event_count:,}", border=True)
    columns[1].metric("Registrations", f"{registrations:,}", border=True)
    columns[2].metric("Attendees", f"{attended:,}", border=True)
    columns[3].metric("Attendance rate", f"{attendance_rate:.1f}%", border=True)


def monthly_summary(data: pd.DataFrame) -> pd.DataFrame:
    result = data.groupby("Month", as_index=False)[["Registrations", "Attended"]].sum()
    result["Month"] = pd.Categorical(
        result["Month"], categories=MONTH_ORDER, ordered=True
    )
    return result.sort_values("Month")
