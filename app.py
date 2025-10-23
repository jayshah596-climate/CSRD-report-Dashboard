import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- Page config ---
st.set_page_config(
    page_title="Global CSRD Reports Dashboard",
    layout="wide"
)

EU_LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/b/b7/Flag_of_Europe.svg"


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
st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
        <img src="{EU_LOGO_URL}" alt="European Union logo" width="48" height="48" style="flex-shrink: 0;" />
        <h1 style="font-size: 2rem; font-weight: 700; margin: 0;">Global CSRD Reports Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Charts in columns
st.subheader("🌍 CSRD Reports by Country")
country_data = filtered_df.groupby("Country", as_index=False)["Company"].count()
fig1 = px.bar(country_data, x="Country", y="Company", color="Country")
st.plotly_chart(fig1, use_container_width=True)


# Data table
st.header("📋 Filtered CSRD Report Data")

# Prepare a display-friendly version of the filtered data
display_df = filtered_df.copy()

# Format publication date without time information
if "Publication date" in display_df.columns:
    if pd.api.types.is_datetime64_any_dtype(display_df["Publication date"]):
        display_df["Publication date"] = display_df["Publication date"].dt.strftime("%Y-%m-%d")
    display_df["Publication date"] = display_df["Publication date"].fillna("")

# Convert report links into clickable hyperlinks using the company name as the anchor text
report_link_column = next(
    (col for col in display_df.columns if col.strip().lower() == "report link"),
    None,
)
company_column = next(
    (col for col in display_df.columns if col.strip().lower() == "company"),
    None,
)

if report_link_column and company_column:U+240A
    link_mask = (U+240A
        display_df[report_link_column].notna()U+240A
        & (display_df[report_link_column].astype(str).str.strip() != "")U+240A
        & display_df[company_column].notna()U+240A
    )␊

    def _make_link(row):
        return (
            f'<a href="{row[report_link_column]}" target="_blank">'
            f"{row[company_column]}</a>"
        )

    display_df.loc[link_mask, report_link_column] = display_df.loc[link_mask].apply(
        _make_link,
        axis=1,
    )
    display_df.loc[~link_mask, report_link_column] = (
        display_df.loc[~link_mask, report_link_column].fillna("")
    )

st.markdown(
    """
    <style>
        .csrd-table thead th {
            text-align: center !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    display_df.to_html(escape=False, index=False, classes="csrd-table"),
    unsafe_allow_html=True,
)

# --- Contact & credits section ---
st.markdown("---")
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #0f4c81, #1cb5e0); border-radius: 16px; padding: 2rem; color: white;">
        <h2 style="margin-bottom: 0.5rem;">🤝 Let's Build Impactful ESG Solutions Together</h2>
        <p style="font-size: 1.05rem; line-height: 1.6;">
            Please connect if you would like to develop a similar dashboard or need support with ESG reporting,
            Climate Risk Assessments, or Net Zero strategy aligned with international standards and frameworks.
        </p>
        <div style="display: flex; flex-wrap: wrap; gap: 1.5rem; font-size: 1.05rem;">
            <div>📧 <a href="mailto:jayshah596@gmail.com" style="color: #ffffff; text-decoration: underline;">jayshah596@gmail.com</a></div>
            <div>📞 <a href="tel:+447435996857" style="color: #ffffff; text-decoration: underline;">+44 7435 996857</a></div>
            <div>💼 <a href="https://www.linkedin.com/in/jay-shah-climate/" target="_blank" style="color: #ffffff; text-decoration: underline;">LinkedIn: Jay Shah</a></div>
        </div>
        <div style="margin-top: 1.5rem; font-weight: 600; font-size: 1.1rem;">Developed by Jay Shah</div>
    </div>
    """,
    unsafe_allow_html=True,
)










