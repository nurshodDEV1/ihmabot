"""Admin handlerlari: statistika, operatorlarni boshqarish."""
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import keyboards as kb
from database import db
from filters import IsAdmin
from locales.texts import t, all_texts
from states import AdminOp
from utils import get_lang, show_menu, esc

router = Router()
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


# ---------------------------------------------------------------------------
# Statistika
# ---------------------------------------------------------------------------
@router.message(F.text.in_(all_texts("btn_stats")))
async def show_stats(message: Message, state: FSMContext):
    await state.clear()
    user = await db.get_user(message.from_user.id)
    lang = get_lang(user)
    stats = await db.get_stats()
    await message.answer(t(lang, "stats_text", **stats))


# ---------------------------------------------------------------------------
# Operatorlar
# ---------------------------------------------------------------------------
@router.message(F.text.in_(all_texts("btn_operators")))
async def show_operators(message: Message, state: FSMContext):
    await state.clear()
    user = await db.get_user(message.from_user.id)
    lang = get_lang(user)
    operators = await db.get_operators()

    parts = [t(lang, "operators_title")]
    if not operators:
        parts.append(t(lang, "no_operators"))
    else:
        for op in operators:
            parts.append(t(lang, "operator_item", name=esc(op.get("full_name") or "—"), id=op["user_id"]))
    await message.answer("\n".join(parts), reply_markup=kb.operators_manage_kb(lang))


@router.callback_query(F.data == "adm_add_op")
async def add_operator_start(cq: CallbackQuery, state: FSMContext):
    user = await db.get_user(cq.from_user.id)
    lang = get_lang(user)
    await state.set_state(AdminOp.add_id)
    await cq.message.answer(t(lang, "enter_operator_id"), reply_markup=kb.cancel_kb(lang))
    await cq.answer()


@router.message(AdminOp.add_id, F.text)
async def add_operator_finish(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    lang = get_lang(user)
    digits = "".join(ch for ch in message.text if ch.isdigit())
    if not digits:
        await message.answer(t(lang, "invalid_id"))
        return

    new_id = int(digits)
    await db.set_role(new_id, db.ROLE_OPERATOR)
    await state.clear()
    await message.answer(t(lang, "operator_added", id=new_id))
    await show_menu(message, user)

    # Yangi operatorga xabar berishga harakat qilamiz
    op = await db.get_user(new_id)
    olang = get_lang(op)
    try:
        await message.bot.send_message(new_id, t(olang, "operator_menu"), reply_markup=kb.operator_menu_kb(olang))
    except Exception:
        pass


@router.callback_query(F.data == "adm_rem_op")
async def remove_operator_start(cq: CallbackQuery, state: FSMContext):
    user = await db.get_user(cq.from_user.id)
    lang = get_lang(user)
    await state.set_state(AdminOp.remove_id)
    await cq.message.answer(t(lang, "enter_remove_operator_id"), reply_markup=kb.cancel_kb(lang))
    await cq.answer()


@router.message(AdminOp.remove_id, F.text)
async def remove_operator_finish(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    lang = get_lang(user)
    digits = "".join(ch for ch in message.text if ch.isdigit())
    if not digits:
        await message.answer(t(lang, "invalid_id"))
        return

    target_id = int(digits)
    target = await db.get_user(target_id)
    if not target or target.get("role") != db.ROLE_OPERATOR:
        await message.answer(t(lang, "not_an_operator"))
        return

    await db.set_role(target_id, db.ROLE_CITIZEN)
    await state.clear()
    await message.answer(t(lang, "operator_removed", id=target_id))
    await show_menu(message, user)
