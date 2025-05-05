import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="Marketing Dashboard", layout="wide")

# Title
st.title("📊 Marketing Dashboard Prototype")
st.write("This dashboard is a starting point to visualize your marketing data. Replace the data section with BigQuery or other sources later.")

# Simulated example data
data = {
    'Date': pd.date_range(end=datetime.today(), periods=30),
    'Channel': ['Meta Ads'] * 15 + ['Google Ads'] * 15,
    'Spend': [300 + i * 10 for i in range(15)] + [250 + i * 8 for i in range(15)],
    'Conversions': [20 + i for i in range(15)] + [15 + i for i in range(15)],
}
df = pd.DataFrame(data)

# Filters
channels = st.multiselect("Select Channels", options=df['Channel'].unique(), default=list(df['Channel'].unique()))
filtered_df = df[df['Channel'].isin(channels)]

# Layout: KPIs
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Spend", f"${filtered_df['Spend'].sum():,.0f}")
with col2:
    st.metric("Total Conversions", f"{filtered_df['Conversions'].sum():,.0f}")
with col3:
    roas = filtered_df['Conversions'].sum() / (filtered_df['Spend'].sum() / 100) if filtered_df['Spend'].sum() else 0
    st.metric("ROAS", f"{roas:.2f}")

# Line chart
st.line_chart(filtered_df.groupby('Date')[['Spend', 'Conversions']].sum())
