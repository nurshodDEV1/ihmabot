"""Klaviaturalar (reply va inline)."""
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from locales.texts import t, CATEGORIES, LANGUAGE_NAMES
from database import db


# ---------------------------------------------------------------------------
# Reply klaviaturalar (asosiy menyular)
# ---------------------------------------------------------------------------
def main_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text=t(lang, "btn_new_appeal"))
    b.button(text=t(lang, "btn_my_appeals"))
    b.button(text=t(lang, "btn_check_status"))
    b.button(text=t(lang, "btn_info"))
    b.button(text=t(lang, "btn_language"))
    b.adjust(1, 2, 2)
    return b.as_markup(resize_keyboard=True)


def operator_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text=t(lang, "btn_new_appeals"))
    b.button(text=t(lang, "btn_my_work"))
    b.button(text=t(lang, "btn_language"))
    b.adjust(2, 1)
    return b.as_markup(resize_keyboard=True)


def admin_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text=t(lang, "btn_new_appeals"))
    b.button(text=t(lang, "btn_my_work"))
    b.button(text=t(lang, "btn_stats"))
    b.button(text=t(lang, "btn_operators"))
    b.button(text=t(lang, "btn_language"))
    b.adjust(2, 2, 1)
    return b.as_markup(resize_keyboard=True)


def phone_kb(lang: str) -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text=t(lang, "btn_share_phone"), request_contact=True)
    return b.as_markup(resize_keyboard=True, one_time_keyboard=True)


def skip_cancel_kb(lang: str) -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text=t(lang, "btn_skip"))
    b.button(text=t(lang, "btn_cancel"))
    b.adjust(2)
    return b.as_markup(resize_keyboard=True)


def cancel_kb(lang: str) -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text=t(lang, "btn_cancel"))
    return b.as_markup(resize_keyboard=True)


# ---------------------------------------------------------------------------
# Inline klaviaturalar
# ---------------------------------------------------------------------------
def language_inline_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for code, name in LANGUAGE_NAMES.items():
        b.button(text=name, callback_data=f"lang:{code}")
    b.adjust(1)
    return b.as_markup()


def category_kb(lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for cat in CATEGORIES:
        b.button(text=t(lang, cat), callback_data=f"cat:{cat}")
    b.button(text=t(lang, "btn_cancel"), callback_data="appeal_cancel")
    b.adjust(1)
    return b.as_markup()


def confirm_cancel_kb(lang: str) -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text=t(lang, "btn_confirm"))
    b.button(text=t(lang, "btn_cancel"))
    b.adjust(1)
    return b.as_markup(resize_keyboard=True)


def appeals_list_kb(appeals: list[dict], lang: str, prefix: str) -> InlineKeyboardMarkup:
    """Murojaatlar ro'yxatini tugmalar sifatida chiqaradi."""
    b = InlineKeyboardBuilder()
    for a in appeals:
        # Operator ma'lumotini qo'shamiz (agar biriktirilgan bo'lsa)
        if a.get("operator_id"):
            op_name = a.get("operator_fio") or a.get("operator_name") or "?"
            # Ismning birinchi so'zi va familiya (agar bor bo'lsa)
            name_parts = op_name.strip().split()
            if len(name_parts) > 1:
                short_name = f"{name_parts[0]} {name_parts[-1][0]}."
            else:
                short_name = name_parts[0] if name_parts else "?"
            label = f"№{a['id']} · {t(lang, a['category'])} · 👤 {short_name}"
        else:
            label = f"№{a['id']} · {t(lang, a['category'])}"
        b.button(text=label, callback_data=f"{prefix}:{a['id']}")
    b.adjust(1)
    return b.as_markup()


def appeal_actions_kb(lang: str, appeal: dict) -> InlineKeyboardMarkup | None:
    """Operator uchun murojaat ustida amallar. Amal qolmasa None qaytaradi."""
    is_closed = appeal.get("status") == db.STATUS_CLOSED
    b = InlineKeyboardBuilder()
    has_buttons = False
    if not appeal.get("operator_id") and not is_closed:
        b.button(text=t(lang, "btn_take"), callback_data=f"optake:{appeal['id']}")
        has_buttons = True
    if not is_closed:
        b.button(text=t(lang, "btn_reply"), callback_data=f"opreply:{appeal['id']}")
        b.button(text=t(lang, "btn_close"), callback_data=f"opclose:{appeal['id']}")
        has_buttons = True
    if not has_buttons:
        return None
    b.adjust(1)
    return b.as_markup()


def operators_manage_kb(lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=t(lang, "btn_add_operator"), callback_data="adm_add_op")
    b.button(text=t(lang, "btn_remove_operator"), callback_data="adm_rem_op")
    b.adjust(1)
    return b.as_markup()


def feedback_kb(lang: str, appeal_id: int) -> InlineKeyboardMarkup:
    """Fuqaro javobdan keyin: javob oldim yoki qoniqmadim."""
    b = InlineKeyboardBuilder()
    b.button(text=t(lang, "btn_satisfied"), callback_data=f"satisfied:{appeal_id}")
    b.button(text=t(lang, "btn_not_satisfied"), callback_data=f"notsatisfied:{appeal_id}")
    b.adjust(1)
    return b.as_markup()
