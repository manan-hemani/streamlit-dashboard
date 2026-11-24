import pandas as pd
import streamlit as st
from analytics import get_filtered_data, show_page_intro

data = get_filtered_data()
show_page_intro(
    "Insights and reports",
    "Review descriptive statistics and export reports for the selected records.",
    ":material/insights:",
)

registrations = data["Registrations"]
average_attendance_rate = data["Attendance rate (%)"].mean()
metrics = st.columns(4)
metrics[0].metric("Mean registrations", f"{registrations.mean():.1f}", border=True)
metrics[1].metric("Median registrations", f"{registrations.median():.1f}", border=True)
metrics[2].metric("Standard deviation", f"{registrations.std(ddof=0):.1f}", border=True)
metrics[3].metric(
    "Average attendance rate", f"{average_attendance_rate:.1f}%", border=True
)

st.subheader("Registration distribution")
bins = pd.cut(registrations, bins=10, include_lowest=True)
distribution = (
    bins.value_counts(sort=False)
    .rename_axis("Registration range")
    .reset_index(name="Event records")
)
distribution["Registration range"] = distribution["Registration range"].astype(str)
st.bar_chart(
    distribution,
    x="Registration range",
    y="Event records",
    alt="Number of event records within each registration-count range.",
)

event_totals = (
    data.groupby("Event_Name", as_index=False)["Registrations"]
    .sum()
    .sort_values("Registrations", ascending=False)
)
if not event_totals.empty:
    most_popular = event_totals.iloc[0]
    least_popular = event_totals.iloc[-1]
    st.info(
        f"Most registered event: {most_popular['Event_Name']} "
        f"({int(most_popular['Registrations']):,} registrations)."
    )
    st.info(
        f"Least registered event: {least_popular['Event_Name']} "
        f"({int(least_popular['Registrations']):,} registrations)."
    )

summary = data.groupby(["Event_Name", "Category", "Department"], as_index=False).agg(
    Registrations=("Registrations", "sum"),
    Attended=("Attended", "sum"),
    Capacity=("Capacity", "sum"),
)
summary["Attendance rate (%)"] = (
    summary["Attended"] / summary["Registrations"].replace(0, 1) * 100
)

st.subheader("Download reports")
filtered_csv = (
    data.drop(columns=["Month number"], errors="ignore")
    .to_csv(index=False)
    .encode("utf-8")
)
summary_csv = summary.to_csv(index=False).encode("utf-8")
with st.container(horizontal=True, vertical_alignment="center"):
    st.download_button(
        "Download filtered event data",
        filtered_csv,
        file_name="filtered_event_data.csv",
        mime="text/csv",
        icon=":material/download:",
    )
    st.download_button(
        "Download event summary",
        summary_csv,
        file_name="event_summary.csv",
        mime="text/csv",
        icon=":material/download:",
    )

st.subheader("Filtered event records")
st.dataframe(
    data.drop(columns=["Month number"], errors="ignore").round(1),
    hide_index=True,
    alt="All event records matching the current sidebar filters.",
)
