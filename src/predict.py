import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

model = None
feature_cols = None
category_avg = None

def train(df):
    global model, feature_cols, category_avg

    df = df.copy()

    # -------------------------------
    # FEATURE ENGINEERING
    # -------------------------------
    df["discount_amount"] = df["price"] * (df["discount"] / 100)
    df["final_price"] = df["price"] - df["discount_amount"]

    # -------------------------------
    # CATEGORY IMPACT (🔥 KEY FIX)
    # -------------------------------
    category_avg = df.groupby("product_category")["revenue"].mean().to_dict()

    # -------------------------------
    # ENCODING
    # -------------------------------
    df = pd.get_dummies(df, columns=["product_category"], drop_first=True)

    feature_cols = [col for col in df.columns if col not in [
        "revenue","order_id","order_date","state","product_name"
    ]]

    X = df[feature_cols]
    y = df["revenue"]

    model = RandomForestRegressor(
        n_estimators=150,
        max_depth=12,
        random_state=42
    )

    model.fit(X, y)


def predict(df, price, quantity, discount, month, category):
    global model, feature_cols, category_avg

    if model is None:
        train(df)

    # -------------------------------
    # BASE CALCULATION
    # -------------------------------
    discount_amount = price * (discount / 100)
    final_price = price - discount_amount

    input_dict = {
        "price": price,
        "quantity": quantity,
        "discount": discount,
        "month": month,
        "discount_amount": discount_amount,
        "final_price": final_price
    }

    # CATEGORY ENCODING
    for col in feature_cols:
        if col.startswith("product_category_"):
            input_dict[col] = 1 if col == f"product_category_{category}" else 0

    input_df = pd.DataFrame([input_dict])

    for col in feature_cols:
        if col not in input_df:
            input_df[col] = 0

    input_df = input_df[feature_cols]

    # -------------------------------
    # MODEL PREDICTION
    # -------------------------------
    prediction = model.predict(input_df)[0]

    # -------------------------------
    # 🔥 CATEGORY BOOST (KEY DIFFERENTIATOR)
    # -------------------------------
    if category in category_avg:
        category_factor = category_avg[category] / np.mean(list(category_avg.values()))
        prediction *= category_factor

    # -------------------------------
    # SAFETY FIX
    # -------------------------------
    prediction = max(0, prediction)

    return prediction