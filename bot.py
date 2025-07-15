import config
import text
from cloud import photo_to_text

import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# Стартовое сообщение
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.reply(text.start)


# Ответ на команду /help
@dp.message(Command("help"))
async def start(message: types.Message):
    await message.answer(text.help)


# Получение фото от пользователя
@dp.message(F.photo)
async def get_photo(message: types.Message):
    waiting_message = await message.reply(text=text.waiting, parse_mode=None)
    try:
        photo_id = message.photo[-1].file_id
        photo = await bot.get_file(photo_id)
        file = await bot.download_file(photo.file_path)
    except Exception:
        await waiting_message.edit_text(text=text.download_error, parse_mode=None)
        logger.error("Ошибка при загрузке фото")
    else:
        text_from_photo = await photo_to_text(file.getvalue())
        await waiting_message.edit_text(text=text_from_photo, parse_mode=None)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
