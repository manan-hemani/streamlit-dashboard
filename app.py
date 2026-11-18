import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# Page configurations
st.set_page_config(
    page_title="CHRIST University | Event Analytics", page_icon="📊", layout="wide"
)

# data file path
DATA_FILE = Path(__file__).parent / "event_registrations.csv"
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
    # Load the data from the CSV file and validate required columns
    pass