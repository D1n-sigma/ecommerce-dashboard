# E-commerce Sales & Inventory Dashboard
### End-to-end Business Intelligence project — Python · Plotly Dash · Pandas

[![Live Demo](https://img.shields.io/badge/Live%20Demo-adn301.pythonanywhere.com-1D9E75?style=for-the-badge)](http://adn301.pythonanywhere.com)
[![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)](https://python.org)
[![Dash](https://img.shields.io/badge/Plotly%20Dash-2.x-purple?style=for-the-badge)](https://dash.plotly.com)

---

## Live Dashboard

**[→ Click here to open the dashboard](http://adn301.pythonanywhere.com)**

> Built to demonstrate end-to-end BI capabilities: raw data ingestion, cleaning, feature engineering, KPI analysis, customer segmentation, and interactive web deployment — all without BI tools like Tableau or Power BI.

---

## Business Problem

An e-commerce retailer has 2 years of transactional data (1M+ rows) but no visibility into:
- Which products drive the most revenue?
- When do customers buy — and when do they stop?
- Which customer segments deserve retention focus?
- What are the seasonal revenue patterns?

This dashboard answers all four questions in a single, shareable URL.

---

## Dashboard Preview

| KPI Cards | Monthly Trend |
|-----------|--------------|
| Revenue, Orders, Customers, AOV | Seasonal spikes identified Oct–Nov |

| Top Products | RFM Segmentation |
|-------------|-----------------|
| Ranked by revenue contribution | 5-segment customer classification |

---

## Key Metrics Delivered

| KPI | Value |
|-----|-------|
| Total Revenue | £17,743,429 |
| Total Orders | 36,969 |
| Unique Customers | 5,878 |
| Avg Order Value | £479.95 |

---

## Analytical Methods

**Data Cleaning**
- Removed cancelled transactions (Invoice prefix `C`)
- Dropped anonymous orders (null Customer ID)
- Filtered negative quantities and prices
- Standardized datetime formats

**Feature Engineering**
- `Revenue = Quantity × Price`
- Monthly and day-of-week aggregations
- Rolling averages for trend smoothing

**RFM Customer Segmentation**
- Recency: days since last purchase
- Frequency: number of unique orders
- Monetary: total spend per customer
- Quartile scoring → 5 segments: Champions, Loyal, Potential, At Risk, Lost

---

## Tech Stack

```
Data        → Online Retail II (UCI / Kaggle) — 1M+ rows
Processing  → Python 3.10, Pandas
Visualization → Plotly Express, Plotly Graph Objects
Dashboard   → Plotly Dash
Deployment  → PythonAnywhere (live URL)
Version Control → GitHub
```

---

## Project Structure

```
ecommerce-dashboard/
├── app.py                  # Dash application — layout + all charts
├── requirements.txt        # Python dependencies
├── notebooks/
│   ├── 01_eda.ipynb        # Exploratory data analysis
│   ├── 02_cleaning.ipynb   # Data cleaning pipeline
│   └── 03_analytics.ipynb  # KPI + RFM analysis
└── README.md
```

---

## Run Locally

```bash
git clone https://github.com/D1n-sigma/ecommerce-dashboard.git
cd ecommerce-dashboard
pip install -r requirements.txt

# Place your dataset at: data/online_retail_II.csv
python app.py
# → Open http://localhost:8050
```

---

## What I Can Build For You

If you're an e-commerce or retail business looking for:

- **Sales performance dashboards** — revenue, AOV, conversion trends
- **Inventory health monitoring** — turnover rate, days of inventory, stockout risk
- **Customer segmentation** — RFM analysis, cohort retention, churn prediction
- **Automated reporting** — scheduled data pulls + PDF/email reports

I can deliver a production-ready dashboard in 1–2 weeks.

**→ Let's talk:** [Upwork Profile](https://www.upwork.com)

---

## Dataset

[Online Retail II — UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii)

> Transnational dataset containing all transactions for a UK-based online retail from 01/12/2009 to 09/12/2011.

---

*Built by Adin · Jakarta, Indonesia · Available for remote work worldwide*
