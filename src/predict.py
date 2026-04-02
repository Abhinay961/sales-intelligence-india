import os
import pandas as pd
import numpy as np
import joblib

from sklearn.linear_model import LinearRegression

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models/model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data/processed/data.csv")

os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)


def train_model():
    df = pd.read_csv(DATA_PATH)

    X = df[["price", "quantity", "discount", "month"]]
    y = df["revenue"]

    model = LinearRegression().fit(X, y)

    joblib.dump(model, MODEL_PATH)

    return model


def load_model():
    if not os.path.exists(MODEL_PATH):
        print("Training model...")
        return train_model()
    return joblib.load(MODEL_PATH)


def predict(price, quantity, discount, month):
    model = load_model()

    data = np.array([[price, quantity, discount, month]])
    return model.predict(data)[0]