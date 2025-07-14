import logging
import asyncio
import config

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from cloud import photo_to_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# Стартовое сообщение
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.reply("Привет")


# Получение фото от пользователя
@dp.message(F.photo)
async def get_photo(message: types.Message):
    photo_id = message.photo[-1].file_id
    photo = await bot.get_file(photo_id)
    file = await bot.download_file(photo.file_path)
    text_from_photo = await photo_to_text(file.getvalue())
    await message.reply(text=text_from_photo, parse_mode=None)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
