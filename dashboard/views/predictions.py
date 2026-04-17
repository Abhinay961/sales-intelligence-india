import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def app(df):

    col_p1, col_p2 = st.columns([3, 1])
    with col_p1:
        st.markdown("# 🧠 Sales Decision Engine")
        st.markdown("Optimize pricing, maximize revenue, and simulate business scenarios.")
    with col_p2:
        st.image("https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&q=80&w=800", use_column_width=True)

    # ===============================
    # 🔹 FILTERS IN SIDEBAR
    # ===============================
    st.sidebar.markdown("### ⚙️ Simulation Parameters")

    categories = sorted(df["product_category"].unique())
    states = sorted(df["state"].unique())

    category = st.sidebar.selectbox("📦 Category", categories)
    state = st.sidebar.selectbox("📍 State", states)
    price = st.sidebar.slider("💲 Price", 100, 80000, 1000)
    discount = st.sidebar.slider("🏷️ Discount (%)", 0, 30, 10)
    month = st.sidebar.slider("📅 Month", 1, 12, 6)

    # ===============================
    # 🔹 DEMAND FUNCTION
    # ===============================
    def calculate_demand(price, discount, month, category, state):

        base = 120

        price_factor = max(0.3, 1 - price / 100000)
        discount_factor = 1 + discount / 50
        seasonal = 1 + (month - 6) * 0.05

        category_factor = {
            "Electronics": 0.8,
            "Clothing": 1.3,
            "Home Appliances": 0.9,
            "Beauty": 1.2,
            "Sports": 1.1,
            "Furniture": 0.7
        }

        # 🔥 NEW: STATE IMPACT
        state_factor = {
            "Maharashtra": 1.3,
            "Delhi": 1.2,
            "Karnataka": 1.1,
            "Tamil Nadu": 1.05,
            "Gujarat": 1.0,
            "Uttar Pradesh": 0.95,
            "West Bengal": 0.9,
            "Rajasthan": 0.85
        }

        return int(
            base *
            price_factor *
            discount_factor *
            seasonal *
            category_factor.get(category, 1) *
            state_factor.get(state, 1)
        )

    # ===============================
    # 🔹 RUN ENGINE
    # ===============================
    if st.button("🚀 Run Analysis"):

        demand = calculate_demand(price, discount, month, category, state)
        revenue = price * demand * (1 - discount / 100)
        profit = (price * 0.3) * demand

        # ===============================
        # KPI CARDS
        # ===============================
        c1, c2, c3 = st.columns(3)

        c1.metric("📦 Sales", demand)
        c2.metric("💰 Revenue", f"₹{int(revenue):,}")
        c3.metric("📈 Profit", f"₹{int(profit):,}")

        st.markdown("---")

        # ===============================
        # DEMAND CURVE (PLOTLY)
        # ===============================
        st.subheader("📉 Demand vs Price")

        prices = list(range(500, 80000, 2000))
        demands = [calculate_demand(p, discount, month, category, state) for p in prices]

        chart_df = pd.DataFrame({"Price": prices, "Demand": demands})
        
        fig = px.area(chart_df, x="Price", y="Demand", 
                      title=f"Demand Sensitivity for {category} in {state}",
                      color_discrete_sequence=["#00f2fe"], template="plotly_dark")
        
        # Mark current price
        fig.add_vline(x=price, line_width=3, line_dash="dash", line_color="#ff4b4b", 
                      annotation_text=f"Current: ₹{price}")
                      
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # ===============================
        # 🔥 OPTIMAL PRICE LOGIC
        # ===============================
        best_price = price
        best_profit = profit
        best_revenue = revenue

        for p in range(500, 80000, 1000):
            d = calculate_demand(p, discount, month, category, state)
            r = p * d * (1 - discount / 100)
            pr = (p * 0.3) * d

            if pr > best_profit:
                best_profit = pr
                best_price = p
                best_revenue = r

        st.subheader("🎯 Optimal Pricing Strategy")

        st.success(f"💡 Best Price: ₹{best_price}")
        st.success(f"📈 Max Profit: ₹{int(best_profit):,}")
        st.success(f"💰 Revenue at Optimal Price: ₹{int(best_revenue):,}")

        # ===============================
        # 🧠 EXPLANATION (IMPORTANT)
        # ===============================
        st.markdown("### 📊 Why this works")

        col_w1, col_w2 = st.columns(2)

        with col_w1:
            st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=600", use_column_width=True)
            st.info(
                f"""
                **Mathematical Relationship:**  
                - **Best Price (₹{best_price:,}):** The specific price point that perfectly balances unit demand with unit margin.  
                - **Revenue at Optimal (₹{int(best_revenue):,}):** Total gross income (`Price × Demand`).  
                - **Max Profit (₹{int(best_profit):,}):** Net gain (`Revenue - Cost`). 
                """
            )

        with col_w2:
            st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=600", use_column_width=True)
            st.info(
                f"""
                **The Sweet Spot & Strategy:**  
                Profit is maximized at **₹{best_price:,}**. Raising the price kills demand; lowering it ruins margins.

                👉 In **{state}**, demand is scaled by regional buying power.  
                👉 In **{category}**, customer price sensitivity affects volume.  

                **💡 Executive Strategy:**
                Use **₹{best_price:,}** for maximum profitability. Lower it only for rapid market capture.
                """
            )

        st.markdown("---")

        # ===============================
        # 🔥 DISCOUNT OPTIMIZATION
        # ===============================
        best_discount = discount
        best_profit_d = profit

        for dsc in range(0, 31, 2):
            d = calculate_demand(price, dsc, month, category, state)
            pr = (price * 0.3) * d

            if pr > best_profit_d:
                best_profit_d = pr
                best_discount = dsc

        st.subheader("🏷️ Discount Optimization")

        st.info(f"💡 Best Discount: {best_discount}%")
        st.info(f"📈 Profit at Best Discount: ₹{int(best_profit_d):,}")

        # ===============================
        # 🧠 FINAL INSIGHTS
        # ===============================
        st.markdown("## 📊 Final Business Insight")

        if best_profit > revenue:
            st.success("🚀 Optimized strategy significantly improves profitability")

        if demand > 150:
            st.success("🔥 Strong demand — scale inventory")

        elif demand < 50:
            st.warning("⚠️ Weak demand — consider pricing adjustments")

        if discount > 20:
            st.warning("⚠️ High discount → reduces margins")