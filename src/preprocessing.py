import pandas as pd
import os

def run_preprocessing():

    os.makedirs("data/processed", exist_ok=True)

    df = pd.read_csv("data/raw/sales.csv")

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.month

    df["cost"] = df["price"] * 0.7
    df["profit"] = (df["price"] - df["cost"]) * df["quantity"]

    df.to_csv("data/processed/data.csv", index=False)

    print("✅ Preprocessing Done")


if __name__ == "__main__":
    run_preprocessing()