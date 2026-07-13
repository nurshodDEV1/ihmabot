"""Inson ijtimoiy xizmatlari markazi — murojaatlar boti. Ishga tushirish fayli."""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramConflictError, TelegramUnauthorizedError
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from database import db
from handlers import get_main_router

# Loglar stdout ga chiqadi (terminalda qizil "xato" ko'rinishida chiqmasligi uchun)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("murojaat_bot")


async def main() -> None:
    await db.init_db()
    logger.info("Ma'lumotlar bazasi tayyor.")

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(get_main_router())

    await bot.delete_webhook(drop_pending_updates=True)
    me = await bot.get_me()
    logger.info("Bot ishga tushdi: @%s", me.username)
    logger.info("Bot ishlayapti. To'xtatish uchun Ctrl+C bosing.")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi (Ctrl+C).")
    except TelegramConflictError:
        logger.error(
            "XATO: Bot boshqa joyda allaqachon ishlab turibdi! "
            "Bir vaqtning o'zida faqat BITTA nusxa ishlashi mumkin. "
            "Boshqa terminal yoki serverdagi botni to'xtating va qayta urinib ko'ring."
        )
    except TelegramUnauthorizedError:
        logger.error(
            "XATO: BOT_TOKEN noto'g'ri yoki bekor qilingan. "
            ".env faylidagi tokenni @BotFather orqali tekshiring."
        )
