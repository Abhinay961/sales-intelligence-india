import streamlit as st
import pandas as pd

def app(df):

    st.markdown("## 📊 Sales Intelligence Dashboard")

    col1, col2 = st.columns(2)

    states_list = sorted(df["state"].unique())
    categories_list = sorted(df["product_category"].unique())

    with col1:
        states = st.multiselect(
            "State",
            states_list,
            default=[states_list[0]]
        )

    with col2:
        categories = st.multiselect(
            "Category",
            categories_list,
            default=[categories_list[0]]
        )

    # -------------------------------
    # ✅ DEFINE FILTERED DATA HERE
    # -------------------------------
    filtered_df = df[
        (df["state"].isin(states)) &
        (df["product_category"].isin(categories))
    ]

    if filtered_df.empty:
        st.warning("No data available for selected filters")
        return

    # -------------------------------
    # KPI
    # -------------------------------
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Revenue", f"₹{int(filtered_df['revenue'].sum()):,}")
    c2.metric("Orders", len(filtered_df))
    c3.metric("Profit", f"₹{int(filtered_df['profit'].sum()):,}")
    c4.metric("Avg Order", f"₹{int(filtered_df['revenue'].mean()):,}")

    st.markdown("---")

    # -------------------------------
    # Monthly Trend
    # -------------------------------
    st.subheader("📈 Monthly Sales Trend")

    monthly = filtered_df.groupby("month")["revenue"].sum().reset_index()
    monthly["month"] = monthly["month"].astype(str)

    st.line_chart(monthly.set_index("month"))

    # -------------------------------
    # Charts
    # -------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏷️ Category Revenue")
        st.bar_chart(filtered_df.groupby("product_category")["revenue"].sum())

    with col2:
        st.subheader("🛍️ Product Distribution")
        fig = filtered_df["product_name"].value_counts().plot.pie(autopct="%1.1f%%").figure
        st.pyplot(fig)

    # -------------------------------
    # 🧠 INSIGHTS (NOW SAFE)
    # -------------------------------
    st.markdown("---")
    st.subheader("📊 Key Insights")

    total_rev = filtered_df["revenue"].sum()
    total_profit = filtered_df["profit"].sum()
    avg_order = filtered_df["revenue"].mean()

    top_category = filtered_df.groupby("product_category")["revenue"].sum().idxmax()
    top_product = filtered_df["product_name"].value_counts().idxmax()

    if total_profit > total_rev * 0.25:
        st.success("✅ Strong profitability observed")
    else:
        st.warning("⚠️ Profit margins are low")

    st.write(f"💰 Top Category: **{top_category}**")
    st.write(f"🛍️ Top Product: **{top_product}**")

    if avg_order > 20000:
        st.info("💎 High-value transactions dominate")
    else:
        st.info("📦 Volume-driven sales observed")