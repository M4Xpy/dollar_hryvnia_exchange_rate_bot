import asyncio
import os

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv, find_dotenv

from app.data_base import (
    save_daily_rates_to_xlsx,
    execute_hourly,
    save_exchange_rate_to_db
)

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


@dp.message()
async def answer(message: types.Message) -> None:
    if message.text == "get_exchange_rate":
        save_daily_rates_to_xlsx()
        await message.answer_document(document=types.InputFile("exchange_rate.xlsx"))
    else:
        await message.reply("Sorry , this  command  is  unknown .")


async def main() -> None:
    polling_task = asyncio.create_task(dp.start_polling(bot))
    hourly_task = asyncio.create_task(execute_hourly(save_exchange_rate_to_db))
    await asyncio.gather(polling_task, hourly_task)
