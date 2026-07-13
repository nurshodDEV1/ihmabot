"""Umumiy handlerlar: /start, ro'yxatdan o'tish, til, /cancel, ma'lumot."""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

import keyboards as kb
from database import db
from locales.texts import t, all_texts
from states import Reg
from utils import get_lang, get_role, show_menu, esc

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    uid = message.from_user.id
    await db.add_user(uid, message.from_user.full_name or "Foydalanuvchi", message.from_user.username)
    user = await db.get_user(uid)
    lang = get_lang(user)
    role = get_role(user)

    # Xodimlar (operator/admin) uchun ro'yxatdan o'tish shart emas
    if role in (db.ROLE_ADMIN, db.ROLE_OPERATOR):
        await show_menu(message, user)
        return

    # Fuqaro hali ro'yxatdan o'tmagan bo'lsa — til so'raymiz
    if not user.get("phone"):
        await state.set_state(Reg.language)
        await message.answer(t(lang, "choose_language"), reply_markup=kb.language_inline_kb())
        return

    name = user.get("fio") or message.from_user.full_name
    await message.answer(
        t(lang, "welcome", name=esc(name)),
        reply_markup=kb.main_menu_kb(lang),
    )


@router.callback_query(F.data.startswith("lang:"))
async def cb_language(cq: CallbackQuery, state: FSMContext):
    code = cq.data.split(":", 1)[1]
    await db.update_language(cq.from_user.id, code)
    try:
        await cq.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    current = await state.get_state()
    if current == Reg.language.state:
        # Ro'yxatdan o'tish davomi — telefon so'raymiz
        await state.set_state(Reg.phone)
        await cq.message.answer(t(code, "ask_phone"), reply_markup=kb.phone_kb(code))
    else:
        # Oddiy til almashtirish
        await state.clear()
        user = await db.get_user(cq.from_user.id)
        await cq.message.answer(t(code, "language_changed"))
        await show_menu(cq.message, user)
    await cq.answer()


@router.message(Reg.phone, F.contact)
async def reg_phone_contact(message: Message, state: FSMContext):
    await db.update_phone(message.from_user.id, message.contact.phone_number)
    await _ask_fullname(message, state)


@router.message(Reg.phone, F.text)
async def reg_phone_text(message: Message, state: FSMContext):
    await db.update_phone(message.from_user.id, message.text.strip())
    await _ask_fullname(message, state)


async def _ask_fullname(message: Message, state: FSMContext):
    await state.set_state(Reg.fullname)
    user = await db.get_user(message.from_user.id)
    await message.answer(t(get_lang(user), "ask_fullname"), reply_markup=ReplyKeyboardRemove())


@router.message(Reg.fullname, F.text)
async def reg_fullname(message: Message, state: FSMContext):
    await db.update_fio(message.from_user.id, message.text.strip())
    await _finish_registration(message, state)


async def _finish_registration(message: Message, state: FSMContext):
    await state.clear()
    user = await db.get_user(message.from_user.id)
    lang = get_lang(user)
    name = (user or {}).get("fio") or message.from_user.full_name
    await message.answer(
        t(lang, "welcome", name=esc(name)),
        reply_markup=kb.main_menu_kb(lang),
    )


@router.message(Command("cancel"))
@router.message(F.text.in_(all_texts("btn_cancel")))
async def cancel_any(message: Message, state: FSMContext):
    had_state = await state.get_state()
    await state.clear()
    user = await db.get_user(message.from_user.id)
    lang = get_lang(user)
    if had_state:
        await message.answer(t(lang, "appeal_cancelled"), reply_markup=ReplyKeyboardRemove())
    await show_menu(message, user)


@router.message(F.text.in_(all_texts("btn_language")))
async def change_language(message: Message, state: FSMContext):
    await state.clear()
    user = await db.get_user(message.from_user.id)
    lang = get_lang(user)
    await message.answer(t(lang, "choose_language"), reply_markup=kb.language_inline_kb())


@router.message(F.text.in_(all_texts("btn_info")))
async def show_info(message: Message):
    user = await db.get_user(message.from_user.id)
    lang = get_lang(user)
    await message.answer(t(lang, "info_text"))


# --- Ro'yxatdan o'tishda tugma o'rniga boshqa narsa yuborilsa — qayta so'raymiz ---
@router.message(Reg.language)
async def reg_language_nudge(message: Message):
    user = await db.get_user(message.from_user.id)
    await message.answer(t(get_lang(user), "choose_language"), reply_markup=kb.language_inline_kb())


@router.message(Reg.phone)
async def reg_phone_nudge(message: Message):
    user = await db.get_user(message.from_user.id)
    lang = get_lang(user)
    await message.answer(t(lang, "ask_phone"), reply_markup=kb.phone_kb(lang))


@router.message(Reg.fullname)
async def reg_fullname_nudge(message: Message):
    user = await db.get_user(message.from_user.id)
    await message.answer(t(get_lang(user), "ask_fullname"))
