import streamlit as st
import pandas as pd
import sys, os

# -------------------------------
# PATH SETUP
# -------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

st.set_page_config(page_title="Sales Intelligence", layout="wide")

# -------------------------------
# IMPORT PIPELINE
# -------------------------------
from src.data_generation import generate_data
from src.preprocessing import run_preprocessing

DATA_PATH = os.path.join(BASE_DIR, "data/processed/data.csv")

# -------------------------------
# SAFE DATA LOADER (NO BUG VERSION)
# -------------------------------
def load_data():

    if not os.path.exists(DATA_PATH):
        generate_data()
        run_preprocessing()

    df = pd.read_csv(DATA_PATH)

    # -------------------------------
    # FORCE REQUIRED COLUMNS
    # -------------------------------
    df["revenue"] = df["price"] * df["quantity"] * (1 - df["discount"]/100)
    df["cost"] = df["price"] * 0.7
    df["profit"] = (df["price"] - df["cost"]) * df["quantity"]

    # Safety for UI
    if "product_name" not in df.columns:
        df["product_name"] = "Product"
    if "product_category" not in df.columns:
        df["product_category"] = "General"

    return df

df = load_data()

# -------------------------------
# IMPORT PAGES
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
col1, col2, col3, col4, col5 = st.columns([6,1,1,1,1])

with col1:
    st.markdown("## 🇮🇳 Sales Intelligence Platform")

with col2:
    if st.button("Home"): st.session_state.page = "Home"
with col3:
    if st.button("Predict"): st.session_state.page = "Predict"
with col4:
    if st.button("Report"): st.session_state.page = "Report"
with col5:
    if st.button("Dev"): st.session_state.page = "Dev"

st.markdown("---")

# -------------------------------
# ROUTING
# -------------------------------
if st.session_state.page == "Home":
    home.app(df)

elif st.session_state.page == "Predict":
    predictions.app(df)

elif st.session_state.page == "Report":
    report.app(df)

elif st.session_state.page == "Dev":
    developer.app()