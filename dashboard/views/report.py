import streamlit as st
from reports.generate_report import generate_pdf

def app(df):

    col_r1, col_r2 = st.columns([3, 1])
    with col_r1:
        st.markdown("## 📄 Business Report Generator")
        st.markdown("Generate comprehensive PDF reports for specific regions and categories.")
    with col_r2:
        st.image("https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&q=80&w=800", use_column_width=True)

    # -------------------------------
    # FILTERS IN SIDEBAR
    # -------------------------------
    st.sidebar.markdown("### 📄 Report Parameters")
    
    states = sorted(df["state"].unique())
    categories = sorted(df["product_category"].unique())

    state = st.sidebar.selectbox("Select State", states)
    category = st.sidebar.selectbox("Select Category", categories)

    st.markdown("---")

    # -------------------------------
    # GENERATE REPORT
    # -------------------------------
    st.info(f"Ready to generate report for **{category}** in **{state}**.", icon="ℹ️")
    
    col_btn1, col_btn2 = st.columns([1, 3])
    
    with col_btn1:
        if st.button("📥 Generate Report", use_container_width=True):

            with st.spinner("Generating PDF..."):
                path = generate_pdf(df, state, category)

            st.success("✅ Report Generated successfully!")

            with open(path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Report",
                    data=f,
                    file_name="business_report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )