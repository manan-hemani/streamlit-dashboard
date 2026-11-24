import streamlit as st
from analytics import get_filtered_data, show_page_intro

data = get_filtered_data()
show_page_intro(
    "Event analytics",
    "Compare event popularity, attendance, and capacity utilization.",
    ":material/event_note:",
)

metrics = st.columns(3)
metrics[0].metric("Events analysed", f"{data['Event_ID'].nunique():,}", border=True)
metrics[1].metric(
    "Average registrations", f"{data['Registrations'].mean():.1f}", border=True
)
metrics[2].metric(
    "Average capacity utilization",
    f"{data['Capacity utilization (%)'].mean():.1f}%",
    border=True,
)

st.subheader("Top ten events by registrations")
top_events = data.nlargest(10, "Registrations").sort_values("Registrations")
st.bar_chart(
    top_events,
    x="Event_Name",
    y="Registrations",
    horizontal=True,
    sort=False,
    color="Category",
    alt="Top ten event records ranked by number of registrations.",
)

left, right = st.columns(2)
with left:
    st.subheader("Registrations compared with attendance")
    st.scatter_chart(
        data,
        x="Registrations",
        y="Attended",
        color="Category",
        size="Capacity",
        alt="Each point compares registrations and attendance for an event record.",
    )
with right:
    st.subheader("Capacity utilization by event")
    utilization = data.nlargest(12, "Capacity utilization (%)").sort_values(
        "Capacity utilization (%)"
    )
    st.bar_chart(
        utilization,
        x="Event_Name",
        y="Capacity utilization (%)",
        horizontal=True,
        sort=False,
        alt="Capacity utilization percentages for the twelve highest-utilization event records.",
    )

st.subheader("Event statistics")
display_columns = [
    "Event_Name",
    "Category",
    "Department",
    "Academic_Year",
    "Registrations",
    "Attended",
    "Capacity",
    "Attendance rate (%)",
    "Capacity utilization (%)",
]
st.dataframe(
    data[display_columns].sort_values("Registrations", ascending=False).round(1),
    hide_index=True,
    alt="Event-level registration, attendance, and capacity statistics.",
)
