import streamlit as st
import os
from reports.generate_report import generate_pdf

def app(df):

    st.markdown("## 📄 Business Report")

    total_rev = df["revenue"].sum()
    total_profit = df["profit"].sum()
    orders = len(df)

    c1, c2, c3 = st.columns(3)

    c1.metric("Revenue", f"₹{int(total_rev):,}")
    c2.metric("Profit", f"₹{int(total_profit):,}")
    c3.metric("Orders", orders)

    st.markdown("---")

    # -------------------------------
    # INSIGHTS
    # -------------------------------
    st.subheader("📊 Business Summary")

    top_category = df.groupby("product_category")["revenue"].sum().idxmax()
    top_state = df.groupby("state")["revenue"].sum().idxmax()

    st.write(f"🏆 Top Category: **{top_category}**")
    st.write(f"📍 Top State: **{top_state}**")

    if total_profit > total_rev * 0.25:
        st.success("Strong profitability observed")
    else:
        st.warning("Margins can be improved")

    st.markdown("---")

    # -------------------------------
    # GENERATE + DOWNLOAD REPORT
    # -------------------------------
    if st.button("📥 Generate Report", key="generate_report_btn"):

        file_path = generate_pdf(df)

        st.success("✅ Report Generated Successfully!")

        # 🔥 DOWNLOAD BUTTON
        with open(file_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Report",
                data=f,
                file_name="business_report.pdf",
                mime="application/pdf"
            )