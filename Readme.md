# CHRIST University Events & Registration Analytics Dashboard

A multi-page analytics dashboard built with **Python** and **Streamlit** to explore university event registrations, attendance, capacity utilisation, and departmental participation.

The dashboard brings event and registration data into one place, helping users understand participation patterns across academic years, compare departments, and identify useful trends through interactive filters, metrics, charts, and downloadable reports.

## Features

The application is organised into five pages:

---

**Dashboard overview** High-level summary of event and
registration activity through key
performance indicators and overview
visualisations.

**Event analytics** Explore event-level performance,
event categories, registration
patterns, attendance, and capacity
utilisation.

**Registration analytics** Analyse registration volumes and
attendance/absence patterns across
the selected academic year and
other filters.

**Department analysis** Compare participation across
departments and examine
department-level patterns.

**Insights & reports** Present analytical summaries and
allow users to inspect or download
relevant data.

---

### Dashboard capabilities

- Analyse event and registration data across academic years.
- Filter the dashboard by academic year, event category, and
  department.
- Review key metrics using Streamlit metric components.
- Explore trends and comparisons using native Streamlit charts.
- Inspect tabular data using interactive dataframes.
- Download relevant data through CSV download controls.
- Navigate between pages using Streamlit's multipage navigation.

## Dataset

The dashboard uses `event_registrations.csv` as its data source.

The dataset contains **176 records** covering academic years **2018--19
through 2025--26**.

The project data model includes the following fields:

Column Description

---

- `Event_ID` Unique identifier for an event.
- `Event_Name` Name of the event.
- `Category` Event category.
- `Department` Department associated with the event.
- `Academic_Year` Academic year in which the event was conducted.
- `Month` Month associated with the event.
- `Registrations` Number of registrations recorded.
- `Attended` Number of registered participants who attended.
- `Capacity` Event capacity.

## Technology stack

- **Python** -- application logic and data processing.
- **Streamlit** -- dashboard interface, page navigation, widgets,
  metrics, tables, charts, and downloads.
- **Pandas** -- data loading, cleaning, transformation, grouping, and
  analysis.
- **NumPy** -- numerical operations where required.

### Native Streamlit components

The project follows a native-Streamlit-first approach. The dashboard
uses built-in components, including:

- `st.navigation()` and `st.Page()` for page navigation.
- `st.metric()` for key performance indicators.
- `st.bar_chart()` for categorical comparisons.
- `st.line_chart()` for trends.
- `st.scatter_chart()` for relationship exploration.
- `st.dataframe()` for tabular data.
- `st.download_button()` for downloadable reports.

## Project structure

```text
├── app.py
├── analytics.py
├── event_registrations.csv
├── requirements.txt
├── README.md
│
├── app_pages/
│   ├── overview.py
│   ├── events.py
│   ├── registrations.py
│   ├── departments.py
│   └── insights.py
│
└── .streamlit/
    └── config.toml
```

---

File or directory Responsibility

---

`app.py` Application entry point and page
navigation setup.

`analytics.py` Shared data-processing and
analytical operations.

`app_pages/` Individual dashboard page
implementations.

`event_registrations.csv` Dataset used by the dashboard.

`requirements.txt` Python package dependencies.

`.streamlit/config.toml` Streamlit theme and application
configuration.

`README.md` Project documentation.

---

## Getting started

### 1. Prerequisites

- Python installed on your system.
- `pip` package installer.
- A terminal or command prompt.

### 2. Clone the repository

```bash
git clone https://github.com/manan-hemani/streamlit-dashboard.git
```

### 3. Create and activate a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

For macOS/Linux, activate with

```bash
python3 -m venv .venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit will provide a local URL in the terminal. Open that URL in
your browser; the default address is:

```text
http://localhost:8501
```

## Requirements

The `requirements.txt` file contains the core dependencies:

```text
streamlit>=1.50.0
pandas
numpy
```

## Application workflow

1.  The application starts from `app.py`.
2.  Streamlit navigation loads the dashboard pages from the `app_pages/`
    directory.
3.  The dataset is loaded and processed using the shared analytical
    logic.
4.  Users select the available filters, such as academic year, category,
    and department.
5.  The pages display relevant metrics, charts, and tabular results
    based on the selected filters.
6.  Users can download supported data through the dashboard's download
    controls.

## Streamlit documentation

The implementation is guided by the official Streamlit documentation:

- [Streamlit documentation](https://docs.streamlit.io/)
- [Multipage
  apps](https://docs.streamlit.io/develop/concepts/multipage-apps)
- [Configuration and
  theming](https://docs.streamlit.io/develop/concepts/configuration)
- [Charts](https://docs.streamlit.io/develop/api-reference/charts)
- [API reference](https://docs.streamlit.io/develop/api-reference)

## Developed By

- Manan Hemani
- 2MCA - A
- 2647137
