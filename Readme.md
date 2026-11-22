# CHRIST University Events & Registration Analytics Dashboard

A Python + Streamlit analytics dashboard for exploring event registration and attendance data.

## Included

- Dashboard overview, event analytics, registration analytics, department analysis, and insights/reports
- Filters for academic year, category, and department
- CSV downloads and input validation
- AI Generated Sample Dataset
- Academic years from **2018 to 2026**

## Run locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

For macOS/Linux, activate with

```bash
source venv/bin/activate
```

## CSV columns

`Event_ID`, `Event_Name`, `Category`, `Department`, `Academic_Year`, `Month`, `Registrations`, `Attended`, `Capacity`
