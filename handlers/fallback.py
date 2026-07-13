"""Catch-all: tushunarsiz xabarlar (holatsiz)."""
from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery

from database import db
from locales.texts import t
from utils import get_lang

router = Router()


@router.message(StateFilter(None))
async def unknown_message(message: Message):
    user = await db.get_user(message.from_user.id)
    lang = get_lang(user)
    await message.answer(t(lang, "unknown"))


@router.callback_query()
async def unknown_callback(cq: CallbackQuery):
    await cq.answer()
