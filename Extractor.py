import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine, URL
from sqlalchemy.dialects.postgresql import insert

#get the require data from yahoo finance api
tickers = ["SPY", "QQQ", "^VIX"]
data = yf.download(
    tickers,
    start="1999-01-01",
    interval="1d",
    auto_adjust=False,
    group_by="ticker"
)
if data.empty:
    raise RuntimeError("No data downloaded!")

#convert data into data that easy for database
frames = []

for ticker in tickers:
    ticker_data = data[ticker].copy()
    ticker_data["Ticker"] = ticker
    frames.append(ticker_data)

df = pd.concat(frames)
df.columns.name = None

#clean data
df.index.name = "Date"
df = df.reset_index()
df = df.dropna(subset=["Close"])

#import data to the database
DB_USER = "postgres"
DB_PASSWORD = input("Enter DB password: ")
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "etf_analysis"

db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

engine = create_engine(db_url)

df.columns = [
    str(col).lower().replace(" ", "_")
    for col in df.columns
]
df["date"] = pd.to_datetime(df["date"]).dt.date

#This function use for deal with the situation of pandas to_sql function can't handle the duplicate primary key
def insert_ignore_conflicts(pd_table, connection, keys, data_iter):
    data = [dict(zip(keys, row)) for row in data_iter]
    if not data:
        return 0

    stmt = insert(pd_table.table).values(data)
    stmt = stmt.on_conflict_do_nothing(
        index_elements=["date", "ticker"]
    )

    result = connection.execute(stmt)
    return result.rowcount

with engine.connect() as connection:
    print("Successfully connected to PostgreSQL!")

    #Since pandas to_sql can't handle duplicate primary key by itself, therefore I create a function to handle it.
    df.to_sql(
        name="stock_prices",
        con=connection,
        if_exists="append",
        index=False,
        chunksize=1000,
        method=insert_ignore_conflicts
    )

print("Downloaded data:")
print(df.head())
print("Total records:", len(df))
print(f"Successfully imported!")