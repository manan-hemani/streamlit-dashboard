import numpy as np
import streamlit as st
from analytics import get_filtered_data, show_page_intro

data = get_filtered_data()
show_page_intro(
    "Department analysis",
    "Compare registrations and attendance across academic departments.",
    ":material/account_balance:",
)

department_data = data.groupby("Department", as_index=False).agg(
    Registrations=("Registrations", "sum"),
    Attended=("Attended", "sum"),
    Events=("Event_ID", "nunique"),
)
department_data["Attendance rate (%)"] = np.where(
    department_data["Registrations"] > 0,
    department_data["Attended"] / department_data["Registrations"] * 100,
    0,
)

left, right = st.columns(2)
with left:
    st.subheader("Registrations by department")
    st.bar_chart(
        department_data.sort_values("Registrations"),
        x="Department",
        y="Registrations",
        horizontal=True,
        sort=False,
        alt="Total event registrations for each department.",
    )
with right:
    st.subheader("Attendance rate by department")
    st.bar_chart(
        department_data.sort_values("Attendance rate (%)"),
        x="Department",
        y="Attendance rate (%)",
        horizontal=True,
        sort=False,
        alt="Attendance percentage for each department.",
    )

st.subheader("Department and category comparison")
department_category = data.pivot_table(
    index="Department",
    columns="Category",
    values="Registrations",
    aggfunc="sum",
    fill_value=0,
)
st.dataframe(
    department_category,
    alt="Table comparing department registration totals across event categories.",
)

st.subheader("Department summary")
st.dataframe(
    department_data.sort_values("Registrations", ascending=False).round(1),
    hide_index=True,
    alt="Summary of event counts, registrations, attendance, and attendance rates by department.",
)
