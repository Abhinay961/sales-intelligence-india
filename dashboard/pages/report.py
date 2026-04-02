import streamlit as st
from reports.generate_report import generate_pdf

def app(df):

    st.markdown("## 📄 Business Report Generator")

    # -------------------------------
    # FILTERS
    # -------------------------------
    states = sorted(df["state"].unique())
    categories = sorted(df["product_category"].unique())

    col1, col2 = st.columns(2)

    with col1:
        state = st.selectbox("Select State", states)

    with col2:
        category = st.selectbox("Select Category", categories)

    st.markdown("---")

    # -------------------------------
    # GENERATE REPORT
    # -------------------------------
    if st.button("📥 Generate Report"):

        path = generate_pdf(df, state, category)

        st.success("✅ Report Generated!")

        with open(path, "rb") as f:
            st.download_button(
                label="⬇️ Download Report",
                data=f,
                file_name="business_report.pdf",
                mime="application/pdf"
            )