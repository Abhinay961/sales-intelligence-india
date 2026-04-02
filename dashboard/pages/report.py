import streamlit as st
from reports.generate_report import generate_pdf

def app(df):

    st.title("📊 Business Report")

    st.bar_chart(df.groupby("state")["revenue"].sum())

    st.success("📌 Insights generated from real sales data")

    if st.button("📥 Download Full PDF Report", key="pdf_download"):
        path = generate_pdf(df)

        with open(path, "rb") as f:
            st.download_button(
                label="Download Report",
                data=f,
                file_name="business_report.pdf",
                mime="application/pdf",
                key="download_pdf_final"
            )