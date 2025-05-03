import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="COVID-19 Dashboard - Pakistan", layout="wide")

# Title
st.title("🦠 COVID-19 Dashboard - Pakistan")

# Load dataset
@st.cache_data
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    df = df[df['location'] == 'Pakistan']
    df['date'] = pd.to_datetime(df['date'])
    return df

data = load_data()

# Sidebar - Date filter
st.sidebar.title("📅 Date Filter")
start_date = st.sidebar.date_input("Start Date", data['date'].min().date())
end_date = st.sidebar.date_input("End Date", data['date'].max().date())

# Filter data
filtered = data[(data['date'] >= pd.to_datetime(start_date)) & 
                (data['date'] <= pd.to_datetime(end_date))]

# Metrics
st.subheader("📊 Key Metrics (in selected range)")
col1, col2, col3 = st.columns(3)
col1.metric("Total Cases", f"{int(filtered['total_cases'].max()):,}")
col2.metric("Total Deaths", f"{int(filtered['total_deaths'].max()):,}")
col3.metric("Vaccinated", f"{int(filtered['people_vaccinated'].max()):,}")

# Line chart - Daily new cases
st.subheader("📈 Daily New COVID-19 Cases")
st.line_chart(filtered.set_index('date')['new_cases'])

# Line chart - Daily deaths
st.subheader("📉 Daily COVID-19 Deaths")
st.line_chart(filtered.set_index('date')['new_deaths'])

# Footer
st.markdown("---")
st.markdown("📌 **Data Source:** [Our World in Data](https://ourworldindata.org/coronavirus)")

