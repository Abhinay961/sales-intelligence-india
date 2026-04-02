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

lr = None
xgb = None


def train_models():
    global lr, xgb

    df = pd.read_csv(DATA_PATH)

    X = df[["price", "quantity", "discount", "month"]]
    y = df["revenue"]

    lr = LinearRegression().fit(X, y)
    xgb = XGBRegressor().fit(X, y)

    joblib.dump(lr, lr_path)
    joblib.dump(xgb, xgb_path)


def load_models():
    global lr, xgb

    if lr is not None and xgb is not None:
        return

    if not os.path.exists(lr_path) or not os.path.exists(xgb_path):
        train_models()
    else:
        lr = joblib.load(lr_path)
        xgb = joblib.load(xgb_path)


def predict(price, quantity, discount, month, model="xgb"):
    load_models()

    data = np.array([[price, quantity, discount, month]])

    if model == "lr":
        return lr.predict(data)[0]
    return xgb.predict(data)[0]