import logging
import asyncio
import config as cf

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(cf.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# Стартовое сообщение
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.reply("Привет")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
