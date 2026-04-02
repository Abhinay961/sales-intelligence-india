import pandas as pd
import os

def run_preprocessing():

    os.makedirs("data/processed", exist_ok=True)

    df = pd.read_csv("data/raw/sales.csv")

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.month

    df.to_csv("data/processed/data.csv", index=False)