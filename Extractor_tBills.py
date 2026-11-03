import os
from dotenv import load_dotenv
import requests
import pandas as pd
from datetime import datetime, date
from sqlalchemy import create_engine, URL
from sqlalchemy.dialects.postgresql import insert

# loading data from .env into system environment
load_dotenv()

# getting data from alphavantage API
url = f"https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=3month&apikey={os.getenv("ALPHAVANTAGE_API_KEY")}"
r = requests.get(url).json().get("data", [])
df = pd.DataFrame(r)
print(df.head())
print(df.info())

df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date

df["yield_percent"] = pd.to_numeric(df["value"], errors="coerce")
df["maturity"] = "3month"
df = df.dropna(subset=["date", "yield_percent"])[["date", "maturity", "yield_percent"]]
print(df.head())
print(df.info())
'''
# 2. Transform (Clean strings and drop invalid values)
df = pd.read_json(r)
df.head()


df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
df["yield_percent"] = pd.to_numeric(df["value"], errors="coerce")
df["maturity"] = "3month"
df = df.dropna(subset=["date", "yield_percent"])[["date", "maturity", "yield_percent"]]

# 3. Load (Idempotent DB Insert)
engine = create_engine(URL.create("postgresql+psycopg2", username="postgres", password="password", host="localhost", port=5432, database="etf_analysis"))

def insert_ignore(table, conn, keys, data_iter):
    stmt = insert(table.table).values([dict(zip(keys, row)) for row in data_iter])
    return conn.execute(stmt.on_conflict_do_nothing(index_elements=["date"])).rowcount

with engine.connect() as conn:
    df.to_sql("treasury_yields", con=conn, if_exists="append", index=False, method=insert_ignore)

'''