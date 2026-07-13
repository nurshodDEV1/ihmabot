"""Yordamchi funksiyalar."""
from html import escape as _escape

from aiogram.types import Message

import keyboards as kb
from config import config
from database import db
from locales.texts import t, DEFAULT_LANG


def esc(text) -> str:
    """HTML uchun xavfsiz matn (foydalanuvchi kiritgan matnlarda < > & belgilaridan himoya)."""
    if text is None:
        return ""
    return _escape(str(text), quote=False)


def citizen_name(user: dict | None) -> str:
    """Fuqaroning F.I.Sh (bo'lmasa Telegram ismi) — Telegram profiliga bosiladigan havola."""
    if not user:
        return "—"
    name = user.get("fio") or user.get("full_name") or "Fuqaro"
    return f'<a href="tg://user?id={user["user_id"]}">{esc(name)}</a>'


def citizen_nick(user: dict | None) -> str:
    """Fuqaroning Telegram niki (@username) yoki '—'."""
    if user and user.get("username"):
        return "@" + user["username"]
    return "—"


def get_lang(user: dict | None) -> str:
    if user and user.get("language"):
        return user["language"]
    return DEFAULT_LANG


def get_role(user: dict | None, user_id: int | None = None) -> str:
    """Foydalanuvchi rolini aniqlaydi (config adminlari doim admin)."""
    uid = user_id if user_id is not None else (user or {}).get("user_id")
    if uid in config.admin_ids:
        return db.ROLE_ADMIN
    return (user or {}).get("role", db.ROLE_CITIZEN)


def is_staff(user: dict | None) -> bool:
    return get_role(user) in (db.ROLE_OPERATOR, db.ROLE_ADMIN)


def fmt_date(value) -> str:
    """'2026-07-09 12:34:56' -> '2026-07-09 12:34'."""
    if not value:
        return "—"
    return str(value)[:16]


def status_text(lang: str, status: str) -> str:
    return t(lang, f"status_{status}")


async def show_menu(message: Message, user: dict | None) -> None:
    """Rolga mos asosiy menyuni yuboradi."""
    lang = get_lang(user)
    role = get_role(user)
    if role == db.ROLE_ADMIN:
        await message.answer(t(lang, "admin_menu"), reply_markup=kb.admin_menu_kb(lang))
    elif role == db.ROLE_OPERATOR:
        await message.answer(t(lang, "operator_menu"), reply_markup=kb.operator_menu_kb(lang))
    else:
        await message.answer(t(lang, "main_menu"), reply_markup=kb.main_menu_kb(lang))


async def notify_new_appeal(bot, appeal_id: int) -> None:
    """Barcha operator va adminlarga yangi murojaat haqida xabar beradi."""
    appeal = await db.get_appeal(appeal_id)
    if not appeal:
        return
    citizen = await db.get_user(appeal["user_id"])
    name = citizen_name(citizen)
    preview = appeal["text"]
    if len(preview) > 400:
        preview = preview[:400] + "…"

    for sid in await db.get_staff_ids():
        staff = await db.get_user(sid)
        lang = get_lang(staff)
        text = t(
            lang, "notify_new_appeal",
            number=appeal_id,
            category=t(lang, appeal["category"]),
            name=name,
            text=esc(preview),
        )
        try:
            await bot.send_message(sid, text, reply_markup=kb.appeal_actions_kb(lang, appeal))
        except Exception:
            pass
