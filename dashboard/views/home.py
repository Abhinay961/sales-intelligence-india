import streamlit as st
import pandas as pd
import plotly.express as px

def app(df):

    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("## 📊 Sales Intelligence Dashboard")
        st.markdown("Monitor key performance indicators and explore sales trends.")
    with col_h2:
        st.image("https://images.unsplash.com/photo-1556155092-490a1ba16284?auto=format&fit=crop&q=80&w=800", use_column_width=True)

    # -------------------------------
    # 🔹 FILTERS IN SIDEBAR
    # -------------------------------
    st.sidebar.markdown("### 🔍 Dashboard Filters")
    
    states_list = sorted(df["state"].unique())
    categories_list = sorted(df["product_category"].unique())

    states = st.sidebar.multiselect(
        "State",
        states_list,
        default=states_list[:3] if len(states_list) >= 3 else states_list
    )

    categories = st.sidebar.multiselect(
        "Category",
        categories_list,
        default=categories_list[:3] if len(categories_list) >= 3 else categories_list
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
    # KPI CARDS
    # -------------------------------
    st.markdown("---")
    
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Revenue", f"₹{int(filtered_df['revenue'].sum()):,}")
    c2.metric("Orders", len(filtered_df))
    c3.metric("Profit", f"₹{int(filtered_df['profit'].sum()):,}")
    c4.metric("Avg Order", f"₹{int(filtered_df['revenue'].mean()):,}")

    st.markdown("---")

    # -------------------------------
    # CHARTS WITH PLOTLY
    # -------------------------------
    col_chart1, col_chart2 = st.columns([2, 1])

    with col_chart1:
        st.subheader("📈 Monthly Sales Trend")
        monthly = filtered_df.groupby("month")["revenue"].sum().reset_index()
        monthly["month"] = monthly["month"].astype(str)
        fig_line = px.line(monthly, x="month", y="revenue", markers=True,
                           title="Revenue over Months",
                           color_discrete_sequence=["#00f2fe"], template="plotly_dark")
        fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_line, use_container_width=True)

    with col_chart2:
        st.subheader("🛍️ Category Distribution")
        category_rev = filtered_df.groupby("product_category")["revenue"].sum().reset_index()
        fig_pie = px.pie(category_rev, names="product_category", values="revenue", 
                         title="Revenue Share", hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Pastel, template="plotly_dark")
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("🏷️ Top Performing Products")
    product_rev = filtered_df.groupby("product_name")["revenue"].sum().reset_index().sort_values("revenue", ascending=False).head(10)
    fig_bar = px.bar(product_rev, x="revenue", y="product_name", orientation="h",
                     title="Top 10 Products by Revenue",
                     color_discrete_sequence=["#4facfe"], template="plotly_dark")
    fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bar, use_container_width=True)

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

    CATEGORY_IMAGES = {
        "Electronics": "https://images.unsplash.com/photo-1498049794561-7780e7231661?auto=format&fit=crop&q=80&w=600",
        "Clothing": "https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?auto=format&fit=crop&q=80&w=600",
        "Home Appliances": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&q=80&w=600",
        "Beauty": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&q=80&w=600",
        "Sports": "https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&q=80&w=600",
        "Furniture": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&q=80&w=600"
    }

    PRODUCT_IMAGES = {
        "iPhone": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?auto=format&fit=crop&q=80&w=600",
        "Samsung Galaxy": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&q=80&w=600",
        "Laptop": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&q=80&w=600",
        "Tablet": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&q=80&w=600",
        "Headphones": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&q=80&w=600",
        "Smartwatch": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&q=80&w=600",
        "T-Shirt": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&q=80&w=600",
        "Jeans": "https://images.unsplash.com/photo-1542272604-787c3835535d?auto=format&fit=crop&q=80&w=600",
        "Jacket": "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&q=80&w=600",
        "Kurta": "https://images.unsplash.com/photo-1583391733959-b2014792be5a?auto=format&fit=crop&q=80&w=600",
        "Sneakers": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&q=80&w=600",
        "Hoodie": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&q=80&w=600",
        "TV": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?auto=format&fit=crop&q=80&w=600",
        "Refrigerator": "https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?auto=format&fit=crop&q=80&w=600",
        "Washing Machine": "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&q=80&w=600",
        "Microwave": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?auto=format&fit=crop&q=80&w=600",
        "Air Conditioner": "https://images.unsplash.com/photo-1629853900595-5a21ff4f5eec?auto=format&fit=crop&q=80&w=600",
        "Perfume": "https://images.unsplash.com/photo-1594035910387-fea47794261f?auto=format&fit=crop&q=80&w=600",
        "Skincare Kit": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?auto=format&fit=crop&q=80&w=600",
        "Makeup Kit": "https://images.unsplash.com/photo-1516975080661-460b299e56ab?auto=format&fit=crop&q=80&w=600",
        "Hair Dryer": "https://images.unsplash.com/photo-1522337660859-02fbefca4702?auto=format&fit=crop&q=80&w=600",
        "Cricket Bat": "https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&q=80&w=600",
        "Football": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?auto=format&fit=crop&q=80&w=600",
        "Badminton Racket": "https://images.unsplash.com/photo-1613918431703-b54133ae0804?auto=format&fit=crop&q=80&w=600",
        "Gym Equipment": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&q=80&w=600",
        "Sofa": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&q=80&w=600",
        "Dining Table": "https://images.unsplash.com/photo-1615800098779-1be32e60cccc?auto=format&fit=crop&q=80&w=600",
        "Chair": "https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?auto=format&fit=crop&q=80&w=600",
        "Bed": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&q=80&w=600"
    }

    tab_cat, tab_prod, tab_prof = st.tabs(["💰 Top Category", "🛍️ Top Product", "📈 Profitability Status"])
    
    with tab_cat:
        cat_img = CATEGORY_IMAGES.get(top_category, "https://images.unsplash.com/photo-1542204165-65bf26472b9b?auto=format&fit=crop&q=80&w=600")
        st.image(cat_img, use_column_width=True)
        st.markdown(f"<h3 style='color: #4facfe;'>💰 Top Category</h3><p style='font-size: 20px; font-weight: bold;'>{top_category}</p>", unsafe_allow_html=True)

    with tab_prod:
        prod_img = PRODUCT_IMAGES.get(top_product, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&q=80&w=600")
        st.image(prod_img, use_column_width=True)
        st.markdown(f"<h3 style='color: #4facfe;'>🛍️ Top Product</h3><p style='font-size: 20px; font-weight: bold;'>{top_product}</p>", unsafe_allow_html=True)
        
    with tab_prof:
        if total_profit > total_rev * 0.25:
            st.success("✅ Strong profitability observed across operations")
        else:
            st.warning("⚠️ Profit margins are currently tracking lower than target thresholds")
            
        if avg_order > 20000:
            st.info("💎 High-value transactions dominate the revenue stream")
        else:
            st.info("📦 Volume-driven sales are driving the majority of revenue")