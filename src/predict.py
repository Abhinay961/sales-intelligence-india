import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

lr_path = os.path.join(BASE_DIR, "models/lr.pkl")
xgb_path = os.path.join(BASE_DIR, "models/xgb.pkl")

# -----------------------------
# AUTO TRAIN IF MODEL MISSING
# -----------------------------
if not os.path.exists(lr_path) or not os.path.exists(xgb_path):
    print("⚠️ Models not found. Training now...")

    import subprocess
    subprocess.run(["python", "src/train_model.py"])

# -----------------------------
# LOAD MODELS
# -----------------------------
lr = joblib.load(lr_path)
xgb = joblib.load(xgb_path)

def predict(price, quantity, discount, month, model="xgb"):
    data = np.array([[price, quantity, discount, month]])

    if model == "lr":
        return lr.predict(data)[0]
    return xgb.predict(data)[0]