"""Bot sozlamalari — .env faylidan o'qiladi."""
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    bot_token: str
    admin_ids: list[int]
    db_path: str


def load_config() -> Config:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token or token.startswith("123456789:AAExample"):
        raise ValueError(
            "BOT_TOKEN topilmadi! .env faylini yarating va @BotFather bergan tokenni kiriting.\n"
            "Namuna uchun .env.example fayliga qarang."
        )

    admin_raw = os.getenv("ADMIN_IDS", "")
    admin_ids = [int(x) for x in admin_raw.replace(" ", "").split(",") if x.strip().isdigit()]

    db_path = os.getenv("DB_PATH", "database.db").strip() or "database.db"

    return Config(bot_token=token, admin_ids=admin_ids, db_path=db_path)


config = load_config()
