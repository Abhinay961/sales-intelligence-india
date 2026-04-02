import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
import joblib, os

os.makedirs("models", exist_ok=True)

df = pd.read_csv("data/processed/data.csv")

X = df[["price","quantity","discount","month"]]
y = df["revenue"]

X_train,X_test,y_train,y_test = train_test_split(X,y)

lr = LinearRegression().fit(X_train,y_train)
xgb = XGBRegressor().fit(X_train,y_train)

joblib.dump(lr,"models/lr.pkl")
joblib.dump(xgb,"models/xgb.pkl")

print("✅ Models ready")