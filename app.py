import streamlit as st
import pandas as pd
import os
from google.cloud import bigquery

# Page config
st.set_page_config(page_title="Marketing Dashboard", layout="wide")
st.title("📊 Marketing Dashboard Prototype")

# Authenticate with BigQuery via Streamlit secret
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
client = bigquery.Client()

# Run a query on your uploaded BigQuery table
QUERY = """
    SELECT
      Date,
      Channel,
      SAFE_CAST(`Amount_spent_SEK` AS FLOAT64) AS Spend,
      SAFE_CAST(`Conversions` AS INT64) AS Conversions
    FROM
      `iqoro-marketing.meta_data_test250505.meta_ads_april`
"""
df = client.query(QUERY).to_dataframe()

# Filters
channels = st.multiselect("Select Channels", options=df['Channel'].unique(), default=list(df['Channel'].unique()))
filtered_df = df[df['Channel'].isin(channels)]

# KPI Columns
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Spend", f"${filtered_df['Spend'].sum():,.0f}")
with col2:
    st.metric("Total Conversions", f"{filtered_df['Conversions'].sum():,.0f}")
with col3:
    roas = filtered_df['Conversions'].sum() / (filtered_df['Spend'].sum() / 100) if filtered_df['Spend'].sum() else 0
    st.metric("ROAS", f"{roas:.2f}")

# Line Chart
st.line_chart(filtered_df.groupby('Date')[['Spend', 'Conversions']].sum())
