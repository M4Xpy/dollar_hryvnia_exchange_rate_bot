import asyncio
import os

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


@dp.message()
async def answer(message: types.Message) -> None:
    if message.text == "get_exchange_rate":
        await message.answer_document(
            document=types.InputFile("exchange_rate.xlsx")
        )
    else:
        await message.reply("Sorry , this  command  is  unknown .")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
