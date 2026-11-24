import streamlit as st
from PIL import Image

img = Image.open("assets/Page_Icon.png")

st.set_page_config(
    page_title="Christ University Event Analytics",
    page_icon=img,
    layout="wide",
)

pages = [
    st.Page(
        "app_pages/overview.py",
        title="Dashboard overview",
        icon=":material/dashboard:",
        default=True,
    ),
    st.Page(
        "app_pages/events.py", title="Event analytics", icon=":material/event_note:"
    ),
    st.Page(
        "app_pages/registrations.py",
        title="Registration analytics",
        icon=":material/how_to_reg:",
    ),
    st.Page(
        "app_pages/departments.py",
        title="Department analysis",
        icon=":material/account_balance:",
    ),
    st.Page(
        "app_pages/insights.py",
        title="Insights and reports",
        icon=":material/insights:",
    ),
]

navigation = st.navigation(pages)
navigation.run()
