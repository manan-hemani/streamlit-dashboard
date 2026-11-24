import streamlit as st
from analytics import (
    get_filtered_data,
    show_page_intro,
    show_summary_metrics,
    monthly_summary,
)

data = get_filtered_data()
show_page_intro(
    "Dashboard overview",
    "Review event participation, registrations, and attendance across the selected academic years.",
    ":material/dashboard:",
)
show_summary_metrics(data)

left, right = st.columns(2)
category_data = (
    data.groupby("Category", as_index=False)["Registrations"]
    .sum()
    .sort_values("Registrations", ascending=False)
)
with left:
    st.subheader("Registrations by event category")
    st.bar_chart(
        category_data,
        x="Category",
        y="Registrations",
        alt="Total registrations grouped by event category.",
    )

with right:
    st.subheader("Monthly registration trend")
    monthly = monthly_summary(data)
    st.line_chart(
        monthly,
        x="Month",
        y="Registrations",
        alt="Monthly registration totals across the selected academic years.",
    )

st.subheader("Most popular events")
popular = (
    data.groupby("Event_Name", as_index=False)["Registrations"]
    .sum()
    .nlargest(10, "Registrations")
    .sort_values("Registrations", ascending=True)
)
st.bar_chart(
    popular,
    x="Event_Name",
    y="Registrations",
    horizontal=True,
    sort=False,
    alt="The ten events with the highest registration totals.",
)
