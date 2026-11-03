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
url = f"https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=daily&maturity=3month&apikey={os.getenv("ALPHAVANTAGE_API_KEY")}"
r = requests.get(url).json().get("data", [])
df = pd.DataFrame(r)

# data transform and cleaning
df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
df["yield_percent"] = pd.to_numeric(df["value"], errors="coerce")
df["maturity"] = "3month"
df = df.dropna(subset=["date", "yield_percent"])[["date", "maturity", "yield_percent"]]

print("Downloaded data:")
print(df.head())
print("Total records:", len(df))
print(f"Successfully imported!")