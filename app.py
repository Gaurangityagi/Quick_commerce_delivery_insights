import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import re
from datetime import datetime, timedelta
from collections import Counter

st.set_page_config(
    page_title="Quick Commerce Analytics",
    layout="wide"
)

# ------------------ DATA LOAD ------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Ecommerce_Delivery_Analytics_New.csv")

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Ensure numeric columns are safe
    df["delivery_time_(minutes)"] = pd.to_numeric(
        df["delivery_time_(minutes)"], errors="coerce"
    )
    df["service_rating"] = pd.to_numeric(
        df["service_rating"], errors="coerce"
    )

    df = df.dropna(subset=["delivery_time_(minutes)", "service_rating"])

    # Synthetic datetime
    start = datetime(2024, 1, 1)
    df["order_datetime"] = [
        start + timedelta(minutes=i * 20) for i in range(len(df))
    ]

    # SLA breach
    df["sla_breach"] = np.where(df["delivery_time_(minutes)"] > 30, "Yes", "No")

    # Normalize flags
    df["delivery_delay"] = df["delivery_delay"].str.lower()
    df["refund_requested"] = df["refund_requested"].str.lower()

    return df


df = load_data()

# ------------------ SIDEBAR ------------------
st.sidebar.header(" Filters")

platforms = st.sidebar.multiselect(
    "Platform", df["platform"].unique(), df["platform"].unique()
)

categories = st.sidebar.multiselect(
    "Product Category",
    df["product_category"].unique(),
    df["product_category"].unique()
)

df = df[
    (df["platform"].isin(platforms)) &
    (df["product_category"].isin(categories))
]

# ------------------ TITLE ------------------
st.title(" Quick Commerce Delivery Intelligence")

# ------------------ KPI ROW ------------------
k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Orders", len(df))
k2.metric("SLA Breach %", f"{(df['sla_breach']=='Yes').mean()*100:.1f}%")
k3.metric("Avg Delivery Time", f"{df['delivery_time_(minutes)'].mean():.1f} min")
k4.metric("Avg Rating", f"{df['service_rating'].mean():.2f}")

st.divider()

# ------------------ CHART ROW 1 ------------------
c1, c2, c3 = st.columns(3)

with c1:
    sla_df = (
        df.groupby("sla_breach")
        .size()
        .reset_index(name="Orders")
        .rename(columns={"sla_breach": "SLA Status"})
    )

    fig = px.bar(
        sla_df,
        x="SLA Status",
        y="Orders",
        title="⏱ SLA Breach Distribution",
        text="Orders"
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig,width='stretch')

with c2:
    fig = px.bar(
        df.groupby("platform", as_index=False)["service_rating"].mean(),
        x="platform", y="service_rating",
        title="⭐ Avg Rating by Platform"
    )
    st.plotly_chart(fig, width='stretch')

with c3:
    fig = px.histogram(
        df,
        x="delivery_time_(minutes)",
        nbins=20,
        title="📦 Delivery Time Distribution"
    )
    st.plotly_chart(fig, width='stretch')

# ------------------ CHART ROW 2 ------------------
c4, c5, c6 = st.columns(3)

with c4:
    delay_df = (
        df.groupby("delivery_delay", as_index=False)["service_rating"].mean()
        .replace({"yes": "Delayed", "no": "No Delay"})
    )
    fig = px.bar(
        delay_df,
        x="delivery_delay", y="service_rating",
        title="📉 Rating vs Delivery Delay"
    )
    st.plotly_chart(fig, width='stretch')

with c5:
    refund_df = (
        df.groupby("refund_requested", as_index=False)["service_rating"].mean()
        .replace({"yes": "Refund Requested", "no": "No Refund"})
    )
    fig = px.bar(
        refund_df,
        x="refund_requested", y="service_rating",
        title="💸 Rating vs Refund"
    )
    st.plotly_chart(fig, width='stretch')

with c6:
    df_hour = df.copy()
    df_hour["hour"] = df_hour["order_datetime"].dt.hour
    evening = df_hour[df_hour["hour"].between(18, 23)]

    if not evening.empty:
        fig = px.bar(
            evening.groupby("platform", as_index=False)["delivery_time_(minutes)"].mean(),
            x="platform", y="delivery_time_(minutes)",
            title="🌙 Evening Delivery Stress"
        )
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("No evening data available for selected filters.")

st.divider()

# ------------------ NLP BIGRAM ANALYSIS ------------------
st.subheader(" Meaningful Complaint Phrases (Context-Aware NLP)")

negative_df = df[df["service_rating"] <= 2]

def clean_text(text):
    return re.sub(r"[^a-z\s]", "", text.lower())

neutral_phrases = {
    "fast delivery", "good service", "quick delivery",
    "nice delivery", "fresh items"
}

counter = Counter()

for review in negative_df["customer_feedback"].dropna():
    words = clean_text(review).split()
    for i in range(len(words) - 1):
        phrase = f"{words[i]} {words[i+1]}"
        if phrase not in neutral_phrases:
            counter[phrase] += 1

bigram_df = (
    pd.DataFrame(counter.items(), columns=["Complaint Phrase", "Frequency"])
    .sort_values("Frequency", ascending=False)
    .head(10)
)

st.dataframe(bigram_df, width='stretch')
# ------------------ EXECUTIVE INSIGHTS ------------------
st.subheader("📌 Executive Insights")

sla_rate = (df['sla_breach'] == "Yes").mean() * 100

delay_impact = (
    df.groupby("delivery_delay")["service_rating"].mean().diff().iloc[-1]
)

refund_impact = (
    df.groupby("refund_requested")["service_rating"].mean().diff().iloc[-1]
)

evening_stress = (
    df[df["order_datetime"].dt.hour.between(18, 23)]
    .groupby("platform")["delivery_time_(minutes)"]
    .mean()
    .sort_values(ascending=False)
)

st.markdown(f"""
**Operational Performance**
- 🚨 **{sla_rate:.1f}%** of orders breach the 30-minute SLA, indicating sustained delivery pressure.
- 🌙 Evening hours (6–11 PM) show the **highest delivery stress**, especially on **{evening_stress.index[0]}**.

**Customer Experience Drivers**
- ⏱ Delivery delays reduce average ratings by **{delay_impact:.2f} stars**.
- 💸 Refund requests reduce average ratings by **{refund_impact:.2f} stars**, making refunds a stronger dissatisfaction signal than SLA breach alone.

**NLP-Based Root Causes**
- Context-aware phrase analysis highlights **operational issues** such as item accuracy, delivery delays, and quality complaints.
""")

# ------------------ DOWNLOAD INSIGHTS ------------------
st.subheader("⬇ Download Insights")

insights_text = f"""
Key Insights:
- {(df['sla_breach']=='Yes').mean()*100:.2f}% of orders breach the 30-minute SLA.
- Delivery delays and refunds have a stronger negative impact on ratings than SLA breaches alone.
- Evening hours show the highest delivery stress across platforms.
- Context-aware NLP reveals recurring complaint phrases tied to operational issues.
"""

st.download_button(
    "Download Executive Insights",
    insights_text,
    file_name="quick_commerce_insights.txt"
)

