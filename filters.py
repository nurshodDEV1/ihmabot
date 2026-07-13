"""Rolga asoslangan filtrlar."""
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from config import config
from database import db
from utils import get_role, is_staff


class IsStaff(BaseFilter):
    """Operator yoki admin."""

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        uid = event.from_user.id
        if uid in config.admin_ids:
            return True
        user = await db.get_user(uid)
        return is_staff(user)


class IsAdmin(BaseFilter):
    """Faqat admin."""

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        uid = event.from_user.id
        if uid in config.admin_ids:
            return True
        user = await db.get_user(uid)
        return get_role(user) == db.ROLE_ADMIN
