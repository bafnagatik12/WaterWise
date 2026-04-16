# WaterWise Travel Dashboard 🌍💧

## Overview

The **WaterWise Travel Dashboard** is an interactive application designed to help travelers understand their water usage in different countries and its environmental impact. The app provides country-specific water data, calculates personal water consumption based on user inputs, and suggests a donation amount to offset that usage.

---

## Features

### 🌐 Country Selection

* Users can select from a list of countries via a dropdown menu.
* The app dynamically loads country-specific data from the backend.

### 📊 Water Metrics Display

For each selected country, the dashboard displays:

* **Water Safety Score (1–5)**

  * Color-coded (Red, Orange, Green) for quick interpretation
* **Water Stress Level (%)**

  * Indicates how much of the country’s water supply is being used
* **Average Daily Water Usage (Liters/person/day)**

  * Converted from national-level data to per-capita daily usage

---

### 🧮 Personalized Water Usage Calculator

Users input:

* Number of travel days
* Number of showers
* Average shower duration

The app:

* Estimates total water usage
* Calculates **daily water consumption**
* Generates a **suggested donation amount** based on country-specific water value

---

### 📈 Data Visualization

* Displays a **bar chart comparison** of:

  * Traveler’s daily water usage
  * Local resident’s average daily usage
* Built using Plotly for clear and interactive visualization

---

## Data Source & Processing

* Data is sourced from global water datasets (e.g., AQUASTAT).
* Raw data is cleaned and processed before being used in the app:

  * Standardized country codes
  * Handled missing values
  * Converted total national water usage into **per capita daily usage**

### Key Transformation:

[
"water_usage": (float(row['Average_Usage']) * 10**9 / float(row['Population']) / 365)
]

* Final cleaned dataset is stored as a CSV file and loaded into the backend.

---

## System Architecture

### Frontend (Client)

* Built using **Anvil**
* Handles:

  * User interaction
  * Input validation
  * Display of results and charts

### Backend (Server)

* Python-based server functions using `anvil.server.call`
* Responsible for:

  * Loading and storing country data
  * Performing calculations
  * Returning results to the frontend

---

## Core Functionalities

### 1. Country Data Retrieval

```python
@anvil.server.callable
def get_country_data(country_code):
  return COUNTRIES_DATA.get(country_code)
```

---

### 2. Donation Calculation

```python
total_usage = base_usage + shower_usage
water_value = total_usage * country_value
```

* Uses:

  * Base daily water usage
  * Shower usage (rate × duration)
  * Country-specific water value

---

### 3. Daily Usage Calculation

```python
daily_avg = total_usage / days
```

* Computes average daily water consumption for visualization

---

## Input Validation

The app ensures:

* All input fields are filled
* Inputs are valid numeric values
* A country is selected before calculation

---

## User Experience Design

* Color-coded indicators for intuitive understanding
* Descriptive text explanations for each metric
* Clean and simple interface for accessibility

---

## Challenges

* Standardizing country names and codes across datasets
* Converting large-scale national data into usable per-person metrics
* Handling missing or inconsistent data
* Ensuring smooth communication between frontend and backend

---

## Future Improvements

* Improve accuracy of water valuation model
* Add more granular (regional/city-level) data
* Enhance UI/UX design
* Expand to mobile compatibility

---

## Conclusion

The WaterWise Travel Dashboard bridges data science and sustainability by transforming complex water usage data into an interactive and user-friendly tool. It empowers travelers to make more informed and responsible decisions about their water consumption.

---
