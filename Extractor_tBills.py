import os
from dotenv import load_dotenv
import requests
import pandas as pd
#from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.dialects.postgresql import insert

# loading data from .env into system environment
load_dotenv()

# getting data from alphavantage API
url = f"https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=daily&maturity=3month&apikey={os.getenv("ALPHAVANTAGE_API_KEY")}"
r = requests.get(url).json().get("data", [])
df = pd.DataFrame(r)

# data transform and cleaning
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df[df["date"] >= "1991-01-01"]
df["yield_percent"] = pd.to_numeric(df["value"], errors="coerce")
df["maturity"] = "3month"
df = df.dropna(subset=["date", "yield_percent"])[["date", "maturity", "yield_percent"]]
df = df.sort_values(by = "date", ascending = True).reset_index(drop = True)

print("Downloaded data:")
print(df.head())
print(df.info())
print("Total records:", len(df))
print("Successfully imported!")

db_url = URL.create(
    drivername="postgresql+psycopg2",
    username="jigmisherpa",
    password=None,
    host="localhost",
    port=5432,
    database="etf_analysis"
)

# Creating a SQLAlchemy engine
engine = create_engine(db_url)

df.to_sql(
    name="t_bills_yield",
    con=engine,
    if_exists="replace",
    index=False
)

print(f"Successfully saved {len(df)} rows to PostgreSQL!")
