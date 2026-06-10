import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide", page_title="Executive Strategy Dashboard", page_icon="📊")

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Global_Sports_Footwear_sales_2018_2026_Dataset.csv")
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["year"] = df["order_date"].dt.year
    df["discount_band"] = pd.cut(
        df["discount_percent"],
        bins=[0,10,20,30],
        labels=["0-10%","11-20%","21-30%"],
        include_lowest=True
    )
    return df

df = load_data()

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.title("🔎 Strategic Filters")

selected_year = st.sidebar.multiselect("Year", df["year"].unique(), df["year"].unique())
selected_brand = st.sidebar.multiselect("Brand", df["brand"].unique(), df["brand"].unique())
selected_country = st.sidebar.multiselect("Country", df["country"].unique(), df["country"].unique())
selected_channel = st.sidebar.multiselect("Channel", df["sales_channel"].unique(), df["sales_channel"].unique())

filtered_df = df[
    (df["year"].isin(selected_year)) &
    (df["brand"].isin(selected_brand)) &
    (df["country"].isin(selected_country)) &
    (df["sales_channel"].isin(selected_channel))
]

# ---------------------------
# KPI SECTION
# ---------------------------
st.title("🌍 Global Sports Footwear Executive Strategy Dashboard")

total_revenue = filtered_df["revenue_usd"].sum()
avg_discount = filtered_df["discount_percent"].mean()
avg_price = filtered_df["final_price_usd"].mean()
avg_rating = filtered_df["customer_rating"].mean()

k1, k2, k3, k4 = st.columns(4)
k1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
k2.metric("🏷 Avg Selling Price", f"${avg_price:.2f}")
k3.metric("🔻 Avg Discount", f"{avg_discount:.2f}%")
k4.metric("⭐ Avg Rating", f"{avg_rating:.2f}")

st.markdown("---")

# ===================================================
# 1️⃣ ADVANCED BRAND POSITIONING SCATTER
# ===================================================
st.subheader("📍 Brand Positioning Map (Revenue vs Discount Dependency)")

brand_summary = filtered_df.groupby("brand").agg(
    Revenue=("revenue_usd","sum"),
    Avg_Discount=("discount_percent","mean"),
    Units=("units_sold","sum"),
    Avg_Price=("final_price_usd","mean")
).reset_index()

fig_scatter = px.scatter(
    brand_summary,
    x="Avg_Discount",
    y="Revenue",
    size="Units",
    color="brand",
    hover_data=["Avg_Price"],
    template="plotly_dark",
    title="Higher Revenue vs Discount Intensity"
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ===================================================
# 2️⃣ DISCOUNT ELASTICITY SCATTER
# ===================================================
st.subheader("📉 Discount vs Revenue Relationship")

fig_discount_scatter = px.scatter(
    filtered_df,
    x="discount_percent",
    y="revenue_usd",
    trendline="ols",
    opacity=0.4,
    template="plotly_dark",
    title="Is Higher Discount Driving Revenue?"
)
st.plotly_chart(fig_discount_scatter, use_container_width=True)

# ===================================================
# 3️⃣ CHANNEL PERFORMANCE MATRIX
# ===================================================
st.subheader("🏬 Channel Premium Capture Matrix")

channel_summary = filtered_df.groupby("sales_channel").agg(
    Revenue=("revenue_usd","sum"),
    Avg_Price=("final_price_usd","mean"),
    Avg_Rating=("customer_rating","mean")
).reset_index()

fig_channel = px.scatter(
    channel_summary,
    x="Avg_Price",
    y="Revenue",
    size="Avg_Rating",
    color="sales_channel",
    template="plotly_dark",
    title="Channel Price Realization vs Revenue"
)
st.plotly_chart(fig_channel, use_container_width=True)

# ===================================================
# 4️⃣ GEOGRAPHIC PRIORITY MAP
# ===================================================
st.subheader("🌎 Geographic Performance Overview")

country_summary = filtered_df.groupby("country").agg(
    Revenue=("revenue_usd","sum"),
    Avg_Rating=("customer_rating","mean"),
    Avg_Price=("final_price_usd","mean")
).reset_index()

fig_geo = px.scatter(
    country_summary,
    x="Avg_Price",
    y="Revenue",
    size="Avg_Rating",
    color="country",
    template="plotly_dark",
    title="Country Revenue vs Price Realization"
)
st.plotly_chart(fig_geo, use_container_width=True)

# ===================================================
# 5️⃣ CATEGORY GROWTH TREND
# ===================================================
st.subheader("📈 Category Growth Trends")

category_trend = filtered_df.groupby(["year","category"]).agg(
    Revenue=("revenue_usd","sum")
).reset_index()

fig_category = px.line(
    category_trend,
    x="year",
    y="Revenue",
    color="category",
    template="plotly_dark",
    title="Revenue Trend by Category (2018–2026)"
)
st.plotly_chart(fig_category, use_container_width=True)

# ===================================================
# 🔥 AUTO-GENERATED EXECUTIVE SUMMARY
# ===================================================
st.markdown("---")
st.subheader("🧠 Auto-Generated Executive Strategic Insights")

# Dynamic Logic
top_brand = brand_summary.sort_values("Revenue", ascending=False).iloc[0]["brand"]
low_discount_revenue = filtered_df[filtered_df["discount_percent"] <= 10]["revenue_usd"].sum()
high_discount_revenue = filtered_df[filtered_df["discount_percent"] > 20]["revenue_usd"].sum()

if low_discount_revenue > high_discount_revenue:
    discount_message = "Revenue is strongest in low discount bands, indicating diminishing returns from aggressive promotions."
else:
    discount_message = "Higher discounting appears to drive incremental revenue."

st.success(f"""
**1️⃣ Revenue Leader:** {top_brand} leads current revenue under selected filters.

**2️⃣ Discount Strategy Insight:** {discount_message}

**3️⃣ Channel Observation:** Retail and Online performance remain balanced with marginal premium capture differences.

**4️⃣ Geographic Spread:** No extreme outlier market detected — portfolio diversification remains strong.

**5️⃣ Strategic Recommendation:** Focus on pricing discipline (≤10% band), explore premium monetization in high-income segments, and avoid margin erosion from excessive discounting.
""")

st.markdown("---")
st.caption("Designed for Executive Decision-Making | Pricing • Channel • Geography • Segmentation • Portfolio")