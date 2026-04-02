import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

def generate_data(n=5000):

    os.makedirs("data/raw", exist_ok=True)

    states = ["Maharashtra","Delhi","Karnataka","Tamil Nadu","Gujarat"]

    regions = {
        "Maharashtra":"West",
        "Delhi":"North",
        "Karnataka":"South",
        "Tamil Nadu":"South",
        "Gujarat":"West"
    }

    products = {
        "Electronics": ["Mobile","Laptop","Tablet"],
        "Home Appliances": ["TV","Refrigerator","Washing Machine"],
        "Clothing": ["Shirt","Jeans","Jacket"]
    }

    data = []

    for i in range(n):

        state = random.choice(states)
        region = regions[state]

        category = random.choice(list(products.keys()))
        product = random.choice(products[category])

        price = np.random.randint(500, 20000)
        quantity = np.random.randint(1, 5)
        discount = np.random.choice([0,5,10,15])

        date = datetime(2023,1,1) + timedelta(days=np.random.randint(365))

        revenue = price * quantity * (1 - discount/100)

        data.append([
            i,
            date,
            state,
            region,
            category,
            product,
            price,
            quantity,
            discount,
            revenue
        ])

    df = pd.DataFrame(data, columns=[
        "order_id",
        "order_date",
        "state",
        "region",
        "product_category",
        "product_name",
        "price",
        "quantity",
        "discount",
        "revenue"
    ])

    df.to_csv("data/raw/sales.csv", index=False)
    return df