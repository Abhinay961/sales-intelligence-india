import streamlit as st
import pandas as pd
import numpy as np

def app(df):

    st.markdown("# 🧠 Sales Decision Engine")
    st.markdown("Optimize pricing, maximize revenue, and simulate business scenarios.")

    st.markdown("---")

    # ===============================
    # 🔹 FILTERS
    # ===============================
    col1, col2, col3 = st.columns(3)

    categories = sorted(df["product_category"].unique())
    states = sorted(df["state"].unique())

    with col1:
        category = st.selectbox("📦 Category", categories)

    with col2:
        state = st.selectbox("📍 State", states)

    with col3:
        price = st.slider("💲 Price", 100, 80000, 1000)

    discount = st.slider("🏷️ Discount (%)", 0, 30, 10)
    month = st.slider("📅 Month", 1, 12, 6)

    st.markdown("---")

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
        # DEMAND CURVE
        # ===============================
        st.subheader("📉 Demand vs Price")

        prices = list(range(500, 80000, 2000))
        demands = [calculate_demand(p, discount, month, category, state) for p in prices]

        chart_df = pd.DataFrame({"Price": prices, "Demand": demands})
        st.line_chart(chart_df.set_index("Price"))

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

        st.write(
            f"""
            • The optimal price ₹{best_price} balances **demand and margin**.  
            • At lower prices, demand increases but profit per unit drops.  
            • At higher prices, profit per unit increases but demand falls.  
            • The model finds the **sweet spot where total profit is maximized**.  

            👉 In **{state}**, demand is influenced by regional buying power.  
            👉 In **{category}**, customer sensitivity to price affects sales volume.  

            💡 Strategy:
            - Use this price for **maximum profit**
            - Slightly lower price if your goal is **market capture (higher sales)**
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