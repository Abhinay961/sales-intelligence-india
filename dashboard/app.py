import streamlit as st
import pandas as pd
import sys, os

# -------------------------------
# PATH SETUP
# -------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

st.set_page_config(page_title="Sales Intelligence", layout="wide")

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@300;400;600;700&family=Outfit:wght@500;700;800&display=swap');
    
    /* Dark Neon Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #0a0514, #1b0b3b, #001e36, #050505);
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
        background-attachment: fixed;
    }
    
    /* Make Sidebar and Header blend seamlessly with the background */
    [data-testid="stSidebar"] {
        background-color: transparent !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1); /* subtle separator */
    }
    
    /* Better text colors and NO shadow in sidebar */
    [data-testid="stSidebar"] * {
        text-shadow: none !important;
        color: #e2e8f0; /* Crisp light gray for general sidebar text */
    }
    
    /* Format Sidebar Headers/Subheaders */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        font-family: 'Outfit', sans-serif !important;
        color: #ffb703 !important; /* Amber highlight for sidebar headers */
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 15px;
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 5px;
    }
    
    /* Fix Sidebar Inputs (Dropdowns & Sliders) - Frosted White with Black Text */
    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-baseweb="base-input"],
    [data-testid="stSidebar"] input {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #000000 !important;
        border-radius: 8px;
        text-shadow: none !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #000000 !important;
        text-shadow: none !important;
    }
    
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Global Font Enforcement */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6, p, li, span, div {
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 1.0); /* Stronger shadow for deep contrast */
    }
    
    /* Professional Color Grading & Readability */
    h1, h2 {
        font-family: 'Outfit', sans-serif !important;
        color: #00f2fe !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        text-transform: uppercase;
    }
    
    h3, h4 {
        font-family: 'Outfit', sans-serif !important;
        color: #b026ff !important; /* Magenta highlight for dynamic contrast */
        font-weight: 700 !important;
        font-style: italic;
    }
    
    /* Target Markdown text blocks specifically to increase readability safely */
    .stMarkdown p {
        color: #ffffff !important; /* Brighter white for high visibility */
        font-size: 18px !important;
        line-height: 1.6 !important;
    }
    
    .stMarkdown li {
        color: #e0f7fa !important; /* Bright icy blue to keep theme intact */
        font-size: 17px !important;
        line-height: 1.6 !important;
        margin-bottom: 10px;
    }
    
    /* Fix Alert Box text colors (st.info, st.success, st.warning) */
    [data-testid="stAlert"] * {
        color: #ffffff !important;
        text-shadow: none !important; /* Clean flat text inside colored boxes */
    }

    /* 3D Glassmorphism Cards for Metrics */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.5), inset 0 2px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'Fira Code', monospace !important;
        font-size: 22px !important; /* Smaller font to ensure large revenue/profit numbers fit */
        color: #ffffff !important;
        text-shadow: 2px 2px 5px rgba(0,0,0,1) !important;
    }
    
    [data-testid="stMetricValue"] > div {
        font-family: 'Fira Code', monospace !important;
        font-size: 22px !important;
        color: #ffffff !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #4facfe !important;
        font-weight: 600 !important;
        font-size: 14px !important; /* Slightly smaller label to prevent text wrapping */
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8) !important;
    }
    
    [data-testid="stMetricLabel"] > div {
        color: #4facfe !important;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 40px 0 rgba(0, 242, 254, 0.2), inset 0 2px 0 rgba(255,255,255,0.2);
    }
    
    /* 3D styling for buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px 0 rgba(0, 242, 254, 0.4), inset 0 -2px 0 rgba(0,0,0,0.2) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px 0 rgba(0, 242, 254, 0.6), inset 0 -2px 0 rgba(0,0,0,0.2) !important;
    }
    .stButton>button:active {
        transform: translateY(1px);
        box-shadow: 0 2px 10px 0 rgba(0, 242, 254, 0.4) !important;
    }
    
    /* Make Plotly charts pop with a subtle 3D shadow container */
    [data-testid="stPlotlyChart"] {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Professional 3D Blending for banner images */
    [data-testid="stImage"] img {
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.9), 0 0 15px rgba(0, 242, 254, 0.15); /* 3D deep shadow with subtle cyan glow */
        border: 1px solid rgba(255, 255, 255, 0.15);
        margin-bottom: 20px;
        aspect-ratio: 4 / 3;
        object-fit: cover;
        max-width: 350px !important;
        transition: transform 0.4s ease, box-shadow 0.4s ease;
    }
    
    [data-testid="stImage"] img:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 30px 50px rgba(0, 0, 0, 1), 0 0 30px rgba(0, 242, 254, 0.4); /* Glow intensifies on hover */
    }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

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
from dashboard.views import welcome, home, predictions, report, developer

# -------------------------------
# SESSION STATE DATA
# -------------------------------
if "df" not in st.session_state:
    st.session_state.df = df

# -------------------------------
# WRAPPER FUNCTIONS FOR NAVIGATION
# -------------------------------
def welcome_page():
    welcome.app()

def home_page():
    home.app(st.session_state.df)

def predictions_page():
    predictions.app(st.session_state.df)

def report_page():
    report.app(st.session_state.df)

def dev_page():
    developer.app()

# -------------------------------
# ROUTING WITH ST.NAVIGATION
# -------------------------------
pg = st.navigation([
    st.Page(welcome_page, title="Welcome", icon="👋"),
    st.Page(home_page, title="Dashboard", icon="📊"),
    st.Page(predictions_page, title="Decision Engine", icon="🧠"),
    st.Page(report_page, title="Automated Reports", icon="📄"),
    st.Page(dev_page, title="Developers", icon="👨‍💻")
])

pg.run()