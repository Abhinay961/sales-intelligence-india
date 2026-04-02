import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

os.makedirs("data/raw", exist_ok=True)

states = ["Maharashtra","Delhi","Karnataka","Tamil Nadu","Gujarat","West Bengal","Uttar Pradesh"]
regions_map = {
    "Maharashtra":"West","Delhi":"North","Karnataka":"South",
    "Tamil Nadu":"South","Gujarat":"West","West Bengal":"East","Uttar Pradesh":"North"
}

products_by_region = {
    "North":["Winter Jacket","Heater","Smartphone"],
    "South":["AC","Fan","Laptop"],
    "West":["TV","Refrigerator","Mixer"],
    "East":["Mobile","Headphones","Tablet"]
}

data = []

for i in range(9000):
    state = random.choice(states)
    region = regions_map[state]
    product = random.choice(products_by_region[region])

    price = np.random.randint(500,30000)
    quantity = np.random.randint(1,5)
    discount = np.random.choice([0,5,10,15,20])

    date = datetime(2023,1,1) + timedelta(days=np.random.randint(365))
    weekend = date.weekday()>=5

    if weekend:
        quantity += 1
        discount += 5

    revenue = price * quantity * (1-discount/100)

    data.append([
        i+1,date,state,region,product,
        price,quantity,discount,revenue
    ])

df = pd.DataFrame(data, columns=[
    "order_id","order_date","state","region",
    "product_name","price","quantity","discount","revenue"
])

df.to_csv("data/raw/sales.csv", index=False)
print("✅ India dataset created")