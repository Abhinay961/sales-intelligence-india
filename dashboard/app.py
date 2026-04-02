import streamlit as st
import pandas as pd
import sys, os

# -------------------------------
# PATH FIX
# -------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

st.set_page_config(page_title="Sales Intelligence", layout="wide")

# -------------------------------
# IMPORT DATA FUNCTIONS FIRST
# -------------------------------
from src.data_generation import generate_data
from src.preprocessing import run_preprocessing

# -------------------------------
# ENSURE DATA EXISTS (FIRST STEP)
# -------------------------------
data_path = os.path.join(BASE_DIR, "data/processed/data.csv")

if not os.path.exists(data_path):
    st.warning("⚠️ Generating dataset...")

    generate_data()
    run_preprocessing()

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv(data_path)

# -------------------------------
# IMPORT PAGES (AFTER DATA READY)
# -------------------------------
from dashboard.pages import home, predictions, report, developer

# -------------------------------
# SESSION STATE
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# -------------------------------
# TOP NAV
# -------------------------------
title_col, nav1, nav2, nav3, nav4 = st.columns([6,1,1,1,1])

with title_col:
    st.markdown("## 🇮🇳 Sales Intelligence Platform")

with nav1:
    if st.button("Home"): st.session_state.page="Home"

with nav2:
    if st.button("Predict"): st.session_state.page="Predict"

with nav3:
    if st.button("Report"): st.session_state.page="Report"

with nav4:
    if st.button("Dev"): st.session_state.page="Dev"

st.markdown("---")

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