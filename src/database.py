import pandas as pd
from sqlalchemy import create_engine
import os

os.makedirs("data/database", exist_ok=True)

engine = create_engine("sqlite:///data/database/sales.db")

df = pd.read_csv("data/processed/data.csv")

df.to_sql("sales", engine, if_exists="replace", index=False)

print("✅ Stored in DB")