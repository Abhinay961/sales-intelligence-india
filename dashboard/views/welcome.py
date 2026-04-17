import streamlit as st

def app():
    st.markdown("<h1 style='text-align: center; color: #4facfe;'>🚀 Welcome to Sales Intelligence India</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #a0a0a0;'>An Industry-Grade AI-Powered Sales Analytics & Decision Engine</p>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("<h3 style='color: #00f2fe;'>📖 Project Overview</h3>", unsafe_allow_html=True)

    col_intro1, col_intro2 = st.columns([2, 1])
    with col_intro1:
        st.markdown("""
        The **Sales Intelligence Platform** is an advanced data analytics and machine learning solution designed for the Indian retail market. 
        It helps businesses transition from traditional reporting to **proactive, data-driven decision making**. 
        """)
    with col_intro2:
        st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=800", use_column_width=True)

    col_intro3, col_intro4 = st.columns([1, 2])
    with col_intro3:
        st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=800", use_column_width=True)
    with col_intro4:
        st.markdown("""
        By combining rich visualizations with predictive algorithms, the platform empowers stakeholders to discover hidden sales patterns, 
        optimize pricing strategies, and maximize profitability across different states and product categories.
        """)

    st.markdown("---")

    st.markdown("<h3 style='color: #00f2fe;'>✨ Industry-Level Features</h3>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Interactive Dashboard", "🧠 ML Decision Engine", "📄 Automated Reporting"])

    with tab1:
        st.info("""
        **Interactive Dashboard**
        - Real-time KPI tracking (Revenue, Orders, Margins)
        - Dynamic filtering by Geography & Category
        - High-quality, interactive Plotly visualizations
        """, icon="📊")

    with tab2:
        st.success("""
        **ML Decision Engine**
        - Demand Sensitivity Analysis
        - Automated Price Optimization
        - Discount Impact Simulation
        - Regional Buying Power adjustment
        """, icon="🧠")

    with tab3:
        st.warning("""
        **Automated Reporting**
        - One-click PDF generation
        - Formatted business reports ready for executives
        - Context-aware data summarization
        """, icon="📄")

    st.markdown("---")
    
    st.markdown("<h3 style='color: #00f2fe;'>🛠️ How We Built It</h3>", unsafe_allow_html=True)
    
    col_tech1, col_tech2 = st.columns([1, 2])
    with col_tech1:
        st.image("https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&q=80&w=800", use_column_width=True)
    with col_tech2:
        st.markdown("""
        - **Data Engineering:** Simulated robust, highly realistic e-commerce datasets mirroring the Indian market using Pandas and NumPy.
        - **Predictive Modeling:** Developed a robust demand forecasting algorithm that accounts for price elasticity, seasonal variations, and regional economic factors.
        """)

    col_tech3, col_tech4 = st.columns([2, 1])
    with col_tech3:
        st.markdown("""
        - **Frontend Architecture:** Engineered a scalable, multi-page web application using Streamlit's latest navigation APIs and custom CSS for a premium UI/UX.
        - **Visualization:** Integrated Plotly Express for highly interactive, responsive data rendering.
        - **Reporting Pipeline:** Utilized ReportLab to compile dynamic data frames into professional, downloadable PDF reports on the fly.
        """)
    with col_tech4:
        st.image("https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&q=80&w=800", use_column_width=True)

    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        st.markdown("<p style='text-align: center; font-style: italic; color: #888;'>Use the sidebar to navigate to the Dashboard and start exploring!</p>", unsafe_allow_html=True)
