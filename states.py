"""FSM holatlari."""
from aiogram.fsm.state import State, StatesGroup


class Reg(StatesGroup):
    """Ro'yxatdan o'tish."""
    language = State()
    phone = State()
    fullname = State()
    address = State()


class NewAppeal(StatesGroup):
    """Yangi murojaat yaratish."""
    category = State()
    text = State()
    media = State()
    confirm = State()


class CheckStatus(StatesGroup):
    """Ariza raqami bo'yicha holatni tekshirish."""
    tracking = State()


class OpReply(StatesGroup):
    """Operatorning javob yozishi."""
    text = State()


class AdminOp(StatesGroup):
    """Admin: operator qo'shish/o'chirish."""
    add_id = State()
    remove_id = State()
