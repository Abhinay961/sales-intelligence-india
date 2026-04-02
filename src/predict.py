import joblib
import numpy as np
import os
import pandas as pd

from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

lr_path = os.path.join(BASE_DIR, "models/lr.pkl")
xgb_path = os.path.join(BASE_DIR, "models/xgb.pkl")
data_path = os.path.join(BASE_DIR, "data/processed/data.csv")

os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)

# -----------------------------
# TRAIN MODEL IF NOT EXISTS
# -----------------------------
def train_models():
    df = pd.read_csv(data_path)

    X = df[["price", "quantity", "discount", "month"]]
    y = df["revenue"]

    lr = LinearRegression().fit(X, y)
    xgb = XGBRegressor().fit(X, y)

    joblib.dump(lr, lr_path)
    joblib.dump(xgb, xgb_path)

    return lr, xgb

# -----------------------------
# LOAD OR TRAIN
# -----------------------------
if not os.path.exists(lr_path) or not os.path.exists(xgb_path):
    print("⚠️ Models not found → Training now...")
    lr, xgb = train_models()
else:
    lr = joblib.load(lr_path)
    xgb = joblib.load(xgb_path)

# -----------------------------
# PREDICTION FUNCTION
# -----------------------------
def predict(price, quantity, discount, month, model="xgb"):
    data = np.array([[price, quantity, discount, month]])

    if model == "lr":
        return lr.predict(data)[0]
    return xgb.predict(data)[0]