# Quick Commerce Delivery Intelligence Dashboard

## Overview
This project is an end-to-end analytics dashboard built to analyze **quick commerce delivery performance** and **customer experience drivers** using real-world e-commerce order data.  
The focus is on **SLA compliance, delivery delays, refunds, ratings, and complaint patterns**, presented through an interactive Streamlit application.

The project is designed from a **data analyst perspective**, emphasizing business insights, robustness to imperfect data, and stakeholder-ready storytelling.

---

## Key Objectives
- Measure SLA breaches and operational stress
- Identify customer experience drivers impacting ratings
- Analyze delivery delays and refund behavior
- Extract meaningful customer complaints using context-aware NLP
- Present insights in a clean, executive-friendly dashboard

---

## Dataset Description
The dataset contains order-level delivery information including:
- Order and customer identifiers
- Platform (Blinkit, JioMart, etc.)
- Delivery time and SLA indicators
- Customer ratings and feedback text
- Delivery delay and refund flags

Note:
The original dataset contained malformed time values.  
**Synthetic timestamps** were generated to enable time-based analysis (hourly and evening stress patterns).  
No claims are made about real historical timelines.

---

## Feature Engineering
- SLA Breach: Delivery time > 30 minutes
- Synthetic Order Timestamp
- Hour-of-day and evening stress indicators
- Normalized delay and refund flags
- Context-aware complaint phrase extraction (bigrams)

---

## Analysis Performed

### Operational Analysis
- SLA breach rate across platforms
- Delivery time distribution
- Evening delivery stress (6 PM – 11 PM)

### Customer Experience Analysis
- Rating impact of delivery delays
- Rating impact of refund requests
- Comparison of SLA breach vs customer-perceived issues

### NLP-Based Complaint Analysis
- Filtered low-rating reviews (rating ≤ 2)
- Extracted bigram complaint phrases
- Removed neutral and ambiguous phrases
- Identified recurring operational pain points

---

## Dashboard Features
- Interactive filters (platform, product category)
- KPI summary cards
- Modern, compact visualizations using Plotly
- Executive insights section visible on the dashboard
- Downloadable executive summary report

---

## Key Insights (Example)
- Nearly half of the orders breach the 30-minute SLA, indicating operational strain.
- Delivery delays and refund requests have a stronger negative impact on ratings than SLA breach alone.
- Evening hours show consistently higher delivery stress across platforms.
- Complaint phrase analysis highlights recurring issues related to delays, item accuracy, and service quality.

---

## Tech Stack
- Python
- Pandas, NumPy
- Plotly (visualization)
- Streamlit (dashboard)

---

## How to Run Locally

1. Clone the repository
```bash
git clone <repository-url>
cd quick_commerce_insights
```
2. Run the streamlit app

```bash
streamlit run app.py
```
---
## Streamlit app link 
https://quickcommercedeliveryinsights.streamlit.app/
