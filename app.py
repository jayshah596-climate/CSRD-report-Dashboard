import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- Page config ---
st.set_page_config(
    page_title="🌍 Global CSRD Reports Dashboard",
    layout="wide"
)

# --- Load Excel and clean headers ---
@st.cache_data
def load_data():
    df = pd.read_excel("CSRD Dashboard.xlsx")
    df.columns = (
        df.columns
        .str.strip()
        .str.replace("\r", " ", regex=True)
        .str.replace("\n", " ", regex=True)
    )
    return df

df = load_data()

# --- Sidebar filters ---
st.sidebar.header("🔍 Filter Options")

# Country filter
countries = sorted(df["Country"].dropna().unique().tolist())
selected_countries = st.sidebar.multiselect(
    "Select Country:", 
    countries
)

# Industry filter
industries = sorted(df["SASB industry (SICS® Industries)"].dropna().unique().tolist())
selected_industries = st.sidebar.multiselect(
    "Select Industry (SASB SICS):", 
    industries
)

# Date range filter
min_date = min(df["Publication date"])
max_date = max(df["Publication date"])
date_range = st.sidebar.date_input(
    "Select Publication Date Range:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Reset button
if st.sidebar.button("Reset Filters", type="secondary"):
    st.experimental_rerun()

# Convert date_range tuple to pandas datetime
date_start = pd.to_datetime(date_range[0])
date_end = pd.to_datetime(date_range[1])

# Update the filtering logic
filtered_df = df.copy()
if selected_countries:
    filtered_df = filtered_df[filtered_df["Country"].isin(selected_countries)]
if selected_industries:
    filtered_df = filtered_df[filtered_df["SASB industry (SICS® Industries)"].isin(selected_industries)]
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["Publication date"].dt.date >= date_start.date()) & 
        (filtered_df["Publication date"].dt.date <= date_end.date())
    ]

# --- Main content ---
st.title("🌍 Global CSRD Reports Dashboard")

# Charts in columns
col1, col2 = st.columns(2)

with col1:
    # Country bar chart
    country_counts = filtered_df.groupby("Country")["Company"].count().reset_index()
    fig1 = px.bar(
        country_counts,
        x="Country",
        y="Company",
        title="Number of CSRD Reports by Country",
        color="Country"
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Industry pie chart
    fig2 = px.pie(
        filtered_df,
        names="SASB industry (SICS® Industries)",
        title="Distribution of Reports by Industry"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Data table
st.header("📋 Filtered CSRD Report Data")
st.dataframe(filtered_df, use_container_width=True)
