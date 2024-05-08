import asyncio
import sqlite3
from datetime import datetime
from typing import Callable

import pandas as pd

from app.parse import get_exchange_rate


def get_current_date_and_time() -> tuple[str, str]:
    current_datetime = datetime.now()
    return (
        current_datetime.strftime("%Y-%m-%d"),
        current_datetime.strftime("%H:%M:%S"),
    )


def save_exchange_rate_to_db() -> None:
    conn = sqlite3.connect("exchange_rates.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS exchange_rates
                 (date TEXT, time TEXT, rate REAL)"""
    )
    date, time = get_current_date_and_time()
    exchange_rate = get_exchange_rate()
    c.execute(
        "INSERT INTO exchange_rates VALUES (?, ?, ?)",
        (date, time, exchange_rate),
    )
    conn.commit()
    conn.close()


def save_daily_rates_to_xlsx() -> None:
    current_date = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect("exchange_rates.db")
    query = f"""SELECT time as datetime, rate as exchange_rate
    FROM exchange_rates
    WHERE date = '{current_date}'"""
    data = pd.read_sql_query(query, conn)
    conn.close()

    data.to_excel("exchange_rate.xlsx", index=False)


async def execute_hourly(func: Callable) -> None:
    next_hour = datetime.now().hour
    while True:
        while next_hour == datetime.now().hour:
            await asyncio.sleep(1)
        next_hour = datetime.now().hour
        func()
        await asyncio.sleep(3570)
