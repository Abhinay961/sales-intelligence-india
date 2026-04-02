import streamlit as st
import pandas as pd
import sys, os

# Fix imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dashboard.pages import home, predictions, report, developer

st.set_page_config(page_title="Sales Intelligence", layout="wide")

# Load data
df = pd.read_csv("data/processed/data.csv")

# -------------------------------
# SESSION STATE (IMPORTANT)
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# -------------------------------
# TOP NAVIGATION (RIGHT CORNER)
# -------------------------------
title_col, nav1, nav2, nav3, nav4 = st.columns([6,1,1,1,1])

with title_col:
    st.markdown("## 🇮🇳 Sales Intelligence Platform")

with nav1:
    if st.button("Home", key="nav_home"):
        st.session_state.page = "Home"

with nav2:
    if st.button("Predict", key="nav_predict"):
        st.session_state.page = "Predict"

with nav3:
    if st.button("Report", key="nav_report"):
        st.session_state.page = "Report"

with nav4:
    if st.button("Dev", key="nav_dev"):
        st.session_state.page = "Dev"

# -------------------------------
# ROUTING
# -------------------------------
page = st.session_state.page

if page == "Home":
    home.app(df)

elif page == "Predict":
    predictions.app()

elif page == "Report":
    report.app(df)

elif page == "Dev":
    developer.app()