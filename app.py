import os, urllib.request

DATA_PATH = "online_retail_II.xlsx"

if not os.path.exists(DATA_PATH):
    print("Downloading dataset... (ini hanya terjadi sekali di Render)")
    urllib.request.urlretrieve(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/00502/online_retail_II.xlsx",
        DATA_PATH
    )
    print("Download selesai.")
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# ── 1. LOAD & CLEAN ──────────────────────────────────────────────
df1 = pd.read_excel(DATA_PATH, sheet_name="Year 2009-2010")
df2 = pd.read_excel(DATA_PATH, sheet_name="Year 2010-2011")
df  = pd.concat([df1, df2], ignore_index=True)

df = df[~df["Invoice"].astype(str).str.startswith("C")]
df = df[df["Customer ID"].notna()]
df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]

df["Revenue"]     = df["Quantity"] * df["Price"]
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Month"]       = df["InvoiceDate"].dt.to_period("M").astype(str)
df["DayOfWeek"]   = df["InvoiceDate"].dt.day_name()

# ── 2. KPI ───────────────────────────────────────────────────────
total_revenue   = df["Revenue"].sum()
total_orders    = df["Invoice"].nunique()
total_customers = df["Customer ID"].nunique()
aov             = total_revenue / total_orders

# ── 3. CHARTS ────────────────────────────────────────────────────
# Monthly trend
monthly = df.groupby("Month")["Revenue"].sum().reset_index()
fig_trend = px.line(
    monthly, x="Month", y="Revenue",
    title="Monthly Revenue Trend",
    markers=True,
    labels={"Revenue": "Revenue (£)", "Month": ""},
)
fig_trend.update_traces(line_color="#1D9E75", line_width=2.5)
fig_trend.update_layout(plot_bgcolor="white", hovermode="x unified",
                        yaxis_tickprefix="£", yaxis_tickformat=",.0f")

# Top 10 products
top_products = (
    df.groupby("Description")["Revenue"]
    .sum().sort_values(ascending=False).head(10).reset_index()
)
fig_products = px.bar(
    top_products.sort_values("Revenue"),
    x="Revenue", y="Description", orientation="h",
    title="Top 10 Products by Revenue",
    color="Revenue", color_continuous_scale="Teal",
    labels={"Revenue": "Revenue (£)", "Description": ""},
)
fig_products.update_layout(plot_bgcolor="white", coloraxis_showscale=False,
                           xaxis_tickprefix="£", xaxis_tickformat=",.0f")

# Day of week
day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
daily = (
    df.groupby("DayOfWeek")["Revenue"]
    .sum().reindex(day_order).reset_index()
)
fig_daily = px.bar(
    daily, x="DayOfWeek", y="Revenue",
    title="Revenue by Day of Week",
    color="Revenue", color_continuous_scale="Blues",
    labels={"DayOfWeek": "", "Revenue": "Revenue (£)"},
)
fig_daily.update_layout(plot_bgcolor="white", coloraxis_showscale=False,
                        yaxis_tickprefix="£", yaxis_tickformat=",.0f")

# RFM segmentation
snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
rfm = (
    df.groupby("Customer ID")
    .agg(
        Recency   = ("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
        Frequency = ("Invoice",     "nunique"),
        Monetary  = ("Revenue",     "sum"),
    )
    .reset_index()
)
rfm["R_Score"] = pd.qcut(rfm["Recency"], q=4, labels=[4,3,2,1]).astype(int)
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), q=4, labels=[1,2,3,4]).astype(int)
rfm["M_Score"] = pd.qcut(rfm["Monetary"], q=4, labels=[1,2,3,4]).astype(int)
rfm["RFM_Score"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]

def segment(score):
    if score >= 10: return "Champions"
    elif score >= 8: return "Loyal"
    elif score >= 6: return "Potential"
    elif score >= 4: return "At Risk"
    else:            return "Lost"

rfm["Segment"] = rfm["RFM_Score"].apply(segment)

seg_summary = (
    rfm.groupby("Segment")
    .agg(Customers=("Customer ID","count"))
    .reset_index()
    .sort_values("Customers", ascending=False)
)
color_map = {
    "Champions": "#1D9E75", "Loyal": "#378ADD",
    "Potential": "#EF9F27", "At Risk": "#D85A30", "Lost": "#E24B4A",
}
fig_rfm = px.bar(
    seg_summary, x="Segment", y="Customers",
    color="Segment", color_discrete_map=color_map,
    title="Customer Segmentation — RFM",
    text="Customers",
    labels={"Customers": "Number of Customers", "Segment": ""},
)
fig_rfm.update_traces(textposition="outside")
fig_rfm.update_layout(plot_bgcolor="white", showlegend=False)

# ── 4. LAYOUT ────────────────────────────────────────────────────
CARD = {
    "background": "white",
    "border": "1px solid #e5e7eb",
    "borderRadius": "10px",
    "padding": "20px 24px",
    "flex": "1",
    "minWidth": "160px",
}
LABEL = {"fontSize": "13px", "color": "#6b7280", "marginBottom": "6px"}
VALUE = {"fontSize": "26px", "fontWeight": "600", "color": "#111827", "margin": "0"}

app = Dash(__name__)
app.title = "E-commerce Sales Dashboard"

app.layout = html.Div(
    style={"fontFamily": "sans-serif", "background": "#f9fafb",
           "minHeight": "100vh", "padding": "32px 40px"},
    children=[

        # Header
        html.H1("E-commerce Sales & Inventory Dashboard",
                style={"fontSize": "22px", "fontWeight": "600",
                       "color": "#111827", "marginBottom": "4px"}),
        html.P("Online Retail II — UK-based, 2009–2011",
               style={"color": "#6b7280", "fontSize": "14px", "marginTop": "0"}),

        # KPI Cards
        html.Div(style={"display": "flex", "gap": "16px",
                        "flexWrap": "wrap", "marginBottom": "24px"}, children=[
            html.Div(style=CARD, children=[
                html.P("Total Revenue", style=LABEL),
                html.P(f"£{total_revenue:,.0f}", style=VALUE),
            ]),
            html.Div(style=CARD, children=[
                html.P("Total Orders", style=LABEL),
                html.P(f"{total_orders:,}", style=VALUE),
            ]),
            html.Div(style=CARD, children=[
                html.P("Unique Customers", style=LABEL),
                html.P(f"{total_customers:,}", style=VALUE),
            ]),
            html.Div(style=CARD, children=[
                html.P("Avg Order Value", style=LABEL),
                html.P(f"£{aov:,.2f}", style=VALUE),
            ]),
        ]),

        # Row 1 — Trend full width
        html.Div(style={"background": "white", "border": "1px solid #e5e7eb",
                        "borderRadius": "10px", "padding": "8px",
                        "marginBottom": "16px"}, children=[
            dcc.Graph(figure=fig_trend, config={"displayModeBar": False}),
        ]),

        # Row 2 — Products + Day of Week
        html.Div(style={"display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "16px", "marginBottom": "16px"}, children=[
            html.Div(style={"background": "white", "border": "1px solid #e5e7eb",
                            "borderRadius": "10px", "padding": "8px"}, children=[
                dcc.Graph(figure=fig_products, config={"displayModeBar": False}),
            ]),
            html.Div(style={"background": "white", "border": "1px solid #e5e7eb",
                            "borderRadius": "10px", "padding": "8px"}, children=[
                dcc.Graph(figure=fig_daily, config={"displayModeBar": False}),
            ]),
        ]),

        # Row 3 — RFM full width
        html.Div(style={"background": "white", "border": "1px solid #e5e7eb",
                        "borderRadius": "10px", "padding": "8px"}, children=[
            dcc.Graph(figure=fig_rfm, config={"displayModeBar": False}),
        ]),
    ]
)

# jadi ini:
server = app.server

if __name__ == "__main__":
    app.run(debug=False)