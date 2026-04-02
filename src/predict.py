import os
import pandas as pd
import numpy as np
import joblib

from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_PATH = os.path.join(BASE_DIR, "data/processed/data.csv")

os.makedirs(MODEL_DIR, exist_ok=True)

lr_path = os.path.join(MODEL_DIR, "lr.pkl")
xgb_path = os.path.join(MODEL_DIR, "xgb.pkl")


# -------------------------------
# TRAIN MODELS
# -------------------------------
def train_models():
    df = pd.read_csv(DATA_PATH)

    X = df[["price", "quantity", "discount", "month"]]
    y = df["revenue"]

    lr = LinearRegression().fit(X, y)
    xgb = XGBRegressor().fit(X, y)

    joblib.dump(lr, lr_path)
    joblib.dump(xgb, xgb_path)

    return lr, xgb


# -------------------------------
# LOAD OR TRAIN MODELS
# -------------------------------
def load_models():
    if not os.path.exists(lr_path) or not os.path.exists(xgb_path):
        print("⚠️ Models not found → Training...")
        return train_models()
    
    return joblib.load(lr_path), joblib.load(xgb_path)


# -------------------------------
# MAIN PREDICT FUNCTION
# -------------------------------
def predict(price, quantity, discount, month, model="xgb"):

    lr, xgb = load_models()  # ✅ SAFE NOW

    data = np.array([[price, quantity, discount, month]])

    if model == "lr":
        return lr.predict(data)[0]
    return xgb.predict(data)[0]