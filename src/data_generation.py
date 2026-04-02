import pandas as pd
import numpy as np
import os

def generate_data():

    os.makedirs("data/raw", exist_ok=True)

    n = 7000

    states = [
        "Maharashtra","Delhi","Karnataka","Tamil Nadu",
        "Gujarat","Uttar Pradesh","West Bengal","Rajasthan"
    ]

    products = {
        "Electronics": ["iPhone","Samsung Galaxy","Laptop","Tablet","Headphones","Smartwatch"],
        "Clothing": ["T-Shirt","Jeans","Jacket","Kurta","Sneakers","Hoodie"],
        "Home Appliances": ["TV","Refrigerator","Washing Machine","Microwave","Air Conditioner"],
        "Beauty": ["Perfume","Skincare Kit","Makeup Kit","Hair Dryer"],
        "Sports": ["Cricket Bat","Football","Badminton Racket","Gym Equipment"],
        "Furniture": ["Sofa","Dining Table","Chair","Bed"]
    }

    rows = []

    for i in range(n):
        category = np.random.choice(list(products.keys()))
        product = np.random.choice(products[category])

        price = np.random.randint(300, 80000)

        quantity = 1 if category == "Electronics" else np.random.randint(1,6)

        discount = np.random.choice([0,5,10,15,20])

        rows.append([
            i,
            pd.Timestamp("2023-01-01") + pd.Timedelta(days=np.random.randint(365)),
            np.random.choice(states),
            category,
            product,
            price,
            quantity,
            discount
        ])

    df = pd.DataFrame(rows, columns=[
        "order_id","order_date","state",
        "product_category","product_name",
        "price","quantity","discount"
    ])

    df.to_csv("data/raw/sales.csv", index=False)