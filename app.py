import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(
    page_title="CHRIST University | Event Analytics", page_icon="📊", layout="wide"
)

DATA_FILE = Path(__file__).parent / "event_registrations.csv"
REQUIRED = [
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

# Custom Style + Fonts
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Shantell+Sans:ital,wght@0,300..800;1,300..800&display=swap');
html, body, [class*="css"] { font-family: 'Shantell Sans', sans-serif; }
.stApp { background: #f5f7fb; color: #17233c; }
[data-testid="stSidebar"] { background: #111d3a; }
[data-testid="stSidebar"] * { color: #eef3ff !important; }
[data-testid="stSidebar"] .stMultiSelect div, [data-testid="stSidebar"] input { color: #17233c !important; }
.hero {
 background: #141F38;
 padding: 28px 32px; border-radius: 18px; color: white; margin: 4px 0 22px 0;
 box-shadow: 0 10px 28px rgba(24,48,91,.13);
}
.hero h1 {  font-size: 30px; margin: 0 0 6px 0; color: white; }
.hero p { color: #dce8ff; margin: 0; font-size: 14px; }
.kpi {
 background: white; border: 1px solid #e7ebf3; border-radius: 15px;
 padding: 18px 20px; box-shadow: 0 4px 16px rgba(22,39,72,.04); min-height: 112px;
}
.kpi-label { color:#75819a; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:.7px; }
.kpi-value { color:#182747; font-family:Shantell Sans,sans-serif; font-size:29px; font-weight:800; margin-top:7px; }
.kpi-note { color:#8290a8; font-size:11px; margin-top:2px; }
.section-title { font-family:Shantell Sans,sans-serif; font-size:20px; font-weight:800; color:#1b2b4a; margin:18px 0 10px 0; }
.panel { background:white; border:1px solid #e7ebf3; border-radius:15px; padding:16px 18px; }
div[data-testid="stDownloadButton"] button { border-radius:9px; background:#1E4EBC; color:white; font-weight:600; } button:hover { background:#1A3D9C; }
footer { visibility:hidden; }
</style>
""",
    unsafe_allow_html=True,
)


# Load and validate the dataset
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    # Checking for missing reuired columns
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    # Empty dataset check
    if df.empty:
        raise ValueError("The CSV contains no records.")
    for col in [
        "Event_ID",
        "Event_Name",
        "Category",
        "Department",
        "Academic_Year",
        "Month",
    ]:
        df[col] = df[col].astype("string").str.strip()
        if df[col].isna().any() or (df[col] == "").any():
            raise ValueError(f"Blank values found in {col}.")
    # Duplicate check for event_id
    if df["Event_ID"].duplicated().any():
        raise ValueError("Event_ID values must be unique.")
    # Making the data into numeric for further caluclations and validations
    for col in ["Registrations", "Attended", "Capacity"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if df[col].isna().any() or not np.isfinite(df[col]).all():
            raise ValueError(f"{col} must contain valid numeric values.")
        if (df[col] < 0).any() or not np.equal(df[col], np.floor(df[col])).all():
            raise ValueError(f"{col} must contain non-negative whole numbers.")
        df[col] = df[col].astype(int)
    if (df["Attended"] > df["Registrations"]).any():
        raise ValueError("Attended cannot exceed Registrations.")
    if (df["Registrations"] > df["Capacity"]).any():
        raise ValueError("Registrations cannot exceed Capacity.")
    # Checking for valid month names
    valid_months = [
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
    if not df["Month"].isin(valid_months).all():
        raise ValueError("Month must use full month names (e.g. January).")
    # Checking for valid academic year format
    if not df["Academic_Year"].str.match(r"\d{4}-\d{2}$").all():
        raise ValueError("Academic_Year must be in YYYY-YY format.")
    # Calculating additional metrics
    df["Attendance_Rate"] = np.where(
        df["Registrations"] > 0, df["Attended"] / df["Registrations"] * 100, 0
    )
    df["Capacity_Utilization"] = np.where(
        df["Capacity"] > 0, df["Registrations"] / df["Capacity"] * 100, 0
    )
    df["Month_Number"] = df["Month"].map({m: i + 1 for i, m in enumerate(valid_months)})
    return df


# Load the dataset
try:
    data = load_data(DATA_FILE)
except Exception as exc:
    st.error(f"Could not load or validate the dataset: {exc}")
    st.stop()

# SIDEBAR
st.sidebar.markdown("# CHRIST University")
st.sidebar.caption("EVENTS & REGISTRATION ANALYTICS")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard Overview",
        "Event Analytics",
        "Registration Analytics",
        "Department Analysis",
        "Insights & Reports",
    ],
)
st.sidebar.markdown("---")
st.sidebar.markdown("### FILTER DATA")
# Year filter
years = st.sidebar.multiselect(
    "Academic year",
    sorted(data.Academic_Year.unique()),
    default=sorted(data.Academic_Year.unique()),
)
# Category filters
categories = st.sidebar.multiselect(
    "Category", sorted(data.Category.unique()), default=sorted(data.Category.unique())
)
# Department filters
departments = st.sidebar.multiselect(
    "Department",
    sorted(data.Department.unique()),
    default=sorted(data.Department.unique()),
)
# Storing filtered data based on user's choice
filtered = data[
    data.Academic_Year.isin(years)
    & data.Category.isin(categories)
    & data.Department.isin(departments)
].copy()
st.sidebar.markdown("---")
st.sidebar.caption("Dataset: Sample Records")
if filtered.empty:
    st.warning("No records match the selected filters. Change one or more filters.")
    st.stop()


# Helper Functions
def header(title, subtitle):
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def kpi(label, value, note=""):
    st.markdown(
        f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>',
        unsafe_allow_html=True,
    )


def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def chart_layout(fig, height=350):
    fig.update_layout(
        height=height,
        margin=dict(l=12, r=12, t=45, b=12),
        paper_bgcolor="#141F38",
        plot_bgcolor="#EFF3F7",
        font=dict(family="Shantell Sans", color="#52617a"),
        title_font=dict(size=16, color="#1b2b4a"),
    )
    return fig


# Calculating values for KPI
total_events = filtered.Event_ID.nunique()
total_reg = int(filtered.Registrations.sum())
total_att = int(filtered.Attended.sum())
attendance = total_att / total_reg * 100 if total_reg else 0
avg_util = filtered.Capacity_Utilization.mean()

# MAIN LAYOUT
# Dashboard Page
if page == "Dashboard Overview":
    header(
        "Events & Registration Analytics",
        "A view of event participation, attendance and engagement.",
    )
    # Columns for KPIs
    cols = st.columns(4)
    with cols[0]:
        kpi("Total events", f"{total_events:,}", "Events in current selection")
    with cols[1]:
        kpi("Registrations", f"{total_reg:,}", "Total registrations")
    with cols[2]:
        kpi("Attended", f"{total_att:,}", "Recorded attendees")
    with cols[3]:
        kpi("Attendance rate", f"{attendance:.1f}%", "Attended ÷ registrations")
    # Separating into 2 columns for chart display
    left, right = st.columns([1, 1])
    # category-wise registrations PIE CHART
    with left:
        section("Registrations by category")
        cat = filtered.groupby("Category", as_index=False).Registrations.sum()
        fig = px.pie(
            cat,
            names="Category",
            values="Registrations",
            hole=0.58,
            color_discrete_sequence=px.colors.qualitative.Safe,
        )
        st.plotly_chart(chart_layout(fig, 330), use_container_width=True)
    # Month-wise registrations LINE CHART
    with right:
        section("Monthly registration trend")
        # Aggregating registrations and attendance by month
        monthly = filtered.groupby("Month_Number", as_index=False).agg(
            Registrations=("Registrations", "sum"), Attended=("Attended", "sum")
        )
        month_names = {
            i: m
            for i, m in enumerate(
                [
                    "",
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
            )
        }
        monthly["Month"] = monthly.Month_Number.map(month_names)
        fig = px.line(
            monthly.sort_values("Month_Number"),
            x="Month",
            y="Registrations",
            markers=True,
        )
        st.plotly_chart(chart_layout(fig, 330), use_container_width=True)
    # Most popular events BAR CHART
    section("Most popular events")
    popular = (
        filtered.groupby("Event_Name", as_index=False)
        .Registrations.sum()
        .nlargest(7, "Registrations")
        .sort_values("Registrations")
    )
    fig = px.bar(
        popular,
        x="Registrations",
        y="Event_Name",
        orientation="h",
        text="Registrations",
        color="Registrations",
        color_continuous_scale="RdYlGn",
    )
    st.plotly_chart(chart_layout(fig, 330), use_container_width=True)
# Event Analytics Page
elif page == "Event Analytics":
    header(
        "Event Analytics",
        "Compare event popularity, attendance and capacity utilization.",
    )
    # KPIs for event analytics
    a, b, c = st.columns(3)
    with a:
        kpi("Events analysed", f"{total_events}", "Filtered event records")
    with b:
        kpi(
            "Average registrations", f"{filtered.Registrations.mean():.1f}", "Per event"
        )
    with c:
        kpi("Avg. capacity utilization", f"{avg_util:.1f}%", "Registrations ÷ capacity")
    # Top 10 events by registrations BAR CHART
    section("Top 10 events by registrations")
    top = filtered.nlargest(10, "Registrations").sort_values("Registrations")
    fig = px.bar(
        top,
        x="Registrations",
        y="Event_Name",
        orientation="h",
        color="Category",
        text="Registrations",
    )
    st.plotly_chart(chart_layout(fig, 390), use_container_width=True)
    left, right = st.columns(2)
    with left:
        section("Registrations vs attendance")
        fig = px.scatter(
            filtered,
            x="Registrations",
            y="Attended",
            color="Category",
            hover_name="Event_Name",
            size="Capacity",
        )
        st.plotly_chart(chart_layout(fig, 350), use_container_width=True)
    with right:
        section("Capacity utilization by event")
        util = filtered.nlargest(12, "Capacity_Utilization").sort_values(
            "Capacity_Utilization"
        )
        fig = px.bar(
            util,
            x="Capacity_Utilization",
            y="Event_Name",
            orientation="h",
            color="Capacity_Utilization",
            color_continuous_scale="RdYlGn",
        )
        st.plotly_chart(chart_layout(fig, 350), use_container_width=True)
    section("Event statistics")
    st.dataframe(
        filtered[
            [
                "Event_Name",
                "Category",
                "Department",
                "Registrations",
                "Attended",
                "Capacity",
                "Attendance_Rate",
                "Capacity_Utilization",
            ]
        ]
        .sort_values("Registrations", ascending=False)
        .round(1),
        use_container_width=True,
        hide_index=True,
    )
# Registration Analytics Page
elif page == "Registration Analytics":
    header(
        "Registration Analytics",
        "Understand how registrations translate into actual attendance.",
    )
    absent = total_reg - total_att
    # KPIs for registration analytics
    a, b, c = st.columns(3)
    with a:
        kpi("Registered", f"{total_reg:,}", "Total registrations")
    with b:
        kpi("Attended", f"{total_att:,}", "Participants who attended")
    with c:
        kpi("Did not attend", f"{absent:,}", "Registrations minus attendance")
    # 2 columns for pie chart and monthly registrations vs attendance
    left, right = st.columns(2)
    with left:
        section("Attendance breakdown")
        pie = pd.DataFrame(
            {"Status": ["Attended", "Did not attend"], "Count": [total_att, absent]}
        )
        fig = px.pie(
            pie,
            names="Status",
            values="Count",
            hole=0.50,
            color="Status",
            color_discrete_map={"Attended": "#1E4EBC", "Did not attend": "#C68931"},
        )
        st.plotly_chart(chart_layout(fig, 340), use_container_width=True)
    with right:
        section("Monthly registrations vs attendance")
        monthly = filtered.groupby("Month_Number", as_index=False).agg(
            Registrations=("Registrations", "sum"), Attended=("Attended", "sum")
        )
        month_names = {
            i: m
            for i, m in enumerate(
                [
                    "",
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec",
                ]
            )
        }
        monthly["Month"] = monthly.Month_Number.map(month_names)
        fig = px.bar(
            monthly.sort_values("Month_Number"),
            x="Month",
            y=["Registrations", "Attended"],
            barmode="group",
            color_discrete_sequence=["#1E4EBC", "#C68931"],
        )
        st.plotly_chart(chart_layout(fig, 340), use_container_width=True)
    section("Attendance rate by category")
    rates = filtered.groupby("Category", as_index=False).agg(
        Registrations=("Registrations", "sum"), Attended=("Attended", "sum")
    )
    rates["Attendance Rate (%)"] = np.where(
        rates.Registrations > 0, rates.Attended / rates.Registrations * 100, 0
    )
    fig = px.bar(
        rates,
        x="Category",
        y="Attendance Rate (%)",
        text_auto=".1f",
        color="Attendance Rate (%)",
        color_continuous_scale="RdYlGn",
    )
    st.plotly_chart(chart_layout(fig, 320), use_container_width=True)
# Department Analysis Page
elif page == "Department Analysis":
    header(
        "Department Analysis",
        "Compare participation and attendance across academic departments.",
    )
    dept = filtered.groupby("Department", as_index=False).agg(
        Registrations=("Registrations", "sum"),
        Attended=("Attended", "sum"),
        Events=("Event_ID", "nunique"),
    )
    dept["Attendance Rate (%)"] = np.where(
        dept.Registrations > 0, dept.Attended / dept.Registrations * 100, 0
    )
    left, right = st.columns(2)
    with left:
        section("Registrations by department")
        fig = px.bar(
            dept.sort_values("Registrations"),
            x="Registrations",
            y="Department",
            orientation="h",
            color="Registrations",
            color_continuous_scale="RdYlGn",
        )
        st.plotly_chart(chart_layout(fig, 370), use_container_width=True)
    with right:
        section("Attendance rate by department")
        fig = px.bar(
            dept.sort_values("Attendance Rate (%)"),
            x="Attendance Rate (%)",
            y="Department",
            orientation="h",
            color="Attendance Rate (%)",
            color_continuous_scale="RdYlGn",
        )
        st.plotly_chart(chart_layout(fig, 370), use_container_width=True)
    section("Department and category registration heatmap")
    pivot = filtered.pivot_table(
        index="Department",
        columns="Category",
        values="Registrations",
        aggfunc="sum",
        fill_value=0,
    )
    fig, ax = plt.subplots(figsize=(10, max(3, len(pivot) * 0.55)))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="RdYlGn", linewidths=0.5, ax=ax)
    ax.set_xlabel("Category")
    ax.set_ylabel("Department")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    section("Department summary")
    st.dataframe(
        dept.sort_values("Registrations", ascending=False).round(1),
        use_container_width=True,
        hide_index=True,
    )
# Insights & Reports Page
else:
    header(
        "Insights & Reports",
        "Explore descriptive statistics and export the currently filtered data.",
    )
    # Calculating KPIs for insights
    vals = filtered.Registrations
    a, b, c, d = st.columns(4)
    with a:
        kpi("Mean registrations", f"{vals.mean():.1f}", "Average per event")
    with b:
        kpi("Median registrations", f"{vals.median():.1f}", "Middle value")
    with c:
        kpi("Std. deviation", f"{vals.std(ddof=0):.1f}", "Spread of registrations")
    with d:
        kpi(
            "Average attendance",
            f"{filtered.Attendance_Rate.mean():.1f}%",
            "Mean event attendance rate",
        )
    section("Registration distribution")
    fig = px.histogram(
        filtered, x="Registrations", nbins=12, color_discrete_sequence=["#1E4EBC"]
    )
    st.plotly_chart(chart_layout(fig, 330), use_container_width=True)
    grouped = filtered.groupby("Event_Name", as_index=False).agg(
        Registrations=("Registrations", "sum"), Attended=("Attended", "sum")
    )
    if not grouped.empty:
        most = grouped.loc[grouped.Registrations.idxmax()]
        least = grouped.loc[grouped.Registrations.idxmin()]
        x, y = st.columns(2)
        with x:
            st.info(
                f"**Most popular event:** {most.Event_Name} — {int(most.Registrations)} registrations"
            )
        with y:
            st.info(
                f"**Least registered event:** {least.Event_Name} — {int(least.Registrations)} registrations"
            )
    section("Download reports")
    csv_filtered = (
        filtered.drop(columns=["Month_Number"], errors="ignore")
        .to_csv(index=False)
        .encode("utf-8")
    )
    summary = filtered.groupby(
        ["Event_Name", "Category", "Department"], as_index=False
    ).agg(
        Registrations=("Registrations", "sum"),
        Attended=("Attended", "sum"),
        Capacity=("Capacity", "sum"),
    )
    summary["Attendance_Rate"] = np.where(
        summary.Registrations > 0, summary.Attended / summary.Registrations * 100, 0
    )
    l, r = st.columns(2)
    with l:
        st.download_button(
            "Download filtered event data (CSV)",
            csv_filtered,
            "filtered_event_data.csv",
            "text/csv",
            use_container_width=True,
        )
    with r:
        st.download_button(
            "Download event summary (CSV)",
            summary.to_csv(index=False).encode("utf-8"),
            "event_summary.csv",
            "text/csv",
            use_container_width=True,
        )
    section("Filtered records")
    st.dataframe(
        filtered.drop(columns=["Month_Number"], errors="ignore").round(1),
        use_container_width=True,
        hide_index=True,
    )
# Footer
st.caption("CHRIST University Events & Registration Analytics Dashboard")
