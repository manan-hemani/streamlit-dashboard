import pandas as pd
import streamlit as st
from analytics import get_filtered_data, show_page_intro, monthly_summary

data = get_filtered_data()
show_page_intro(
    "Registration analytics",
    "Understand how registrations translate into actual attendance.",
    ":material/how_to_reg:",
)

registrations = int(data["Registrations"].sum())
attended = int(data["Attended"].sum())
did_not_attend = registrations - attended

metrics = st.columns(3)
metrics[0].metric("Registrations", f"{registrations:,}", border=True)
metrics[1].metric("Attended", f"{attended:,}", border=True)
metrics[2].metric("Did not attend", f"{did_not_attend:,}", border=True)

left, right = st.columns(2)
with left:
    st.subheader("Attendance breakdown")
    attendance_data = pd.DataFrame({
        "Status": ["Attended", "Did not attend"],
        "Count": [attended, did_not_attend],
    })
    st.bar_chart(
        attendance_data, x="Status", y="Count",
        alt="Comparison of attendees and registered participants who did not attend.",
    )

with right:
    st.subheader("Monthly registrations and attendance")
    st.bar_chart(
        monthly_summary(data), x="Month", y=["Registrations", "Attended"],
        stack=False, sort=False,
        alt="Monthly totals comparing registrations with attendance.",
    )

st.subheader("Attendance rate by category")
category_rates = (
    data.groupby("Category", as_index=False)[["Registrations", "Attended"]]
    .sum()
)
category_rates["Attendance rate (%)"] = (
    category_rates["Attended"] / category_rates["Registrations"].replace(0, 1) * 100
)
st.bar_chart(
    category_rates, x="Category", y="Attendance rate (%)",
    alt="Attendance percentage for each event category.",
)
