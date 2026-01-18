# CodTech Internship -- Task 1

## API Integration & Data Visualization (Weather Dashboard)

This project fetches real-time weather forecast data from the
**OpenWeatherMap API** and visualizes it using **Python** and
**Matplotlib**.\
It generates a simple dashboard for a selected city (Hyderabad) with
multiple charts.

### Features

-   Calls a public REST API (OpenWeatherMap)
-   Parses and processes JSON data
-   Visualizes:
    -   Temperature & "Feels Like" over time
    -   Humidity and Wind speed
    -   Rainfall (per 3-hour interval)
    -   Most frequent weather conditions
-   Saves the dashboard as an image

------------------------------------------------------------------------

## Requirements

-   Python 3.9+
-   Libraries:
    -   `requests`
    -   `matplotlib`

------------------------------------------------------------------------

## Setup

1.  Create and activate a virtual environment:

``` bash
python3 -m venv weatherenv
source weatherenv/bin/activate
```

2.  Install dependencies:

``` bash
pip install requests matplotlib
```

3.  Get an API key:

-   Sign up at https://openweathermap.org/
-   Go to **Profile → My API Keys**
-   Copy your API key

4.  Set the API key:

``` bash
export OWM_API_KEY="YOUR_OPENWEATHER_API_KEY"
```

------------------------------------------------------------------------

## Run

``` bash
python weather_dashboard.py --city "Hyderabad" --country "IN" --out hyderabad_dashboard.png
```

This will: - Fetch Hyderabad's 5-day weather forecast - Display a
4-panel dashboard - Save the output as `hyderabad_dashboard.png`

------------------------------------------------------------------------

## Files Included

-   `weather_dashboard.py` -- Python script (API + visualization)
-   `hyderabad_dashboard.png` -- Generated dashboard image
-   `README.md` -- Project documentation

------------------------------------------------------------------------

This fulfills **CodTech Internship -- Task 1: API Integration and Data
Visualization**.
