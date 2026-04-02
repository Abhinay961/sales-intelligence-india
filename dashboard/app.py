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
# ENSURE FOLDERS
# -------------------------------
os.makedirs(os.path.join(BASE_DIR, "data/raw"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "data/processed"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)

# -------------------------------
# IMPORT PIPELINE FUNCTIONS
# -------------------------------
from src.data_generation import generate_data
from src.preprocessing import run_preprocessing

data_path = os.path.join(BASE_DIR, "data/processed/data.csv")

# -------------------------------
# LOAD OR FIX DATA PIPELINE
# -------------------------------
def load_or_create_data():
    if not os.path.exists(data_path):
        st.warning("⚠️ Generating dataset...")
        generate_data()
        run_preprocessing()

    df = pd.read_csv(data_path)

    # -------------------------------
    # PIPELINE VALIDATION (CRITICAL FIX)
    # -------------------------------
    required_cols = ["price", "quantity", "discount", "month", "revenue", "profit"]

    if not all(col in df.columns for col in required_cols):
        st.warning("⚠️ Data schema mismatch → regenerating dataset...")
        generate_data()
        run_preprocessing()
        df = pd.read_csv(data_path)

    return df


# -------------------------------
# LOAD DATA SAFELY
# -------------------------------
df = load_or_create_data()

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
# TOP NAVIGATION
# -------------------------------
title_col, nav1, nav2, nav3, nav4 = st.columns([6,1,1,1,1])

with title_col:
    st.markdown("## 🇮🇳 Sales Intelligence Platform")

with nav1:
    if st.button("Home"):
        st.session_state.page = "Home"

with nav2:
    if st.button("Predict"):
        st.session_state.page = "Predict"

with nav3:
    if st.button("Report"):
        st.session_state.page = "Report"

with nav4:
    if st.button("Dev"):
        st.session_state.page = "Dev"

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