"""Fuqaro handlerlari: yangi murojaat, mening murojaatlarim, holat."""
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import keyboards as kb
from database import db
from locales.texts import t, all_texts
from states import NewAppeal, CheckStatus
from utils import get_lang, show_menu, fmt_date, status_text, notify_new_appeal, esc

router = Router()


# ---------------------------------------------------------------------------
# Yangi murojaat
# ---------------------------------------------------------------------------
@router.message(F.text.in_(all_texts("btn_new_appeal")))
async def new_appeal_start(message: Message, state: FSMContext):
    await state.clear()
    user = await db.get_user(message.from_user.id)
    lang = get_lang(user)
    await state.set_state(NewAppeal.category)
    await message.answer(t(lang, "choose_category"), reply_markup=kb.category_kb(lang))


@router.callback_query(NewAppeal.category, F.data == "appeal_cancel")
async def new_appeal_cancel_cb(cq: CallbackQuery, state: FSMContext):
    await state.clear()
    user = await db.get_user(cq.from_user.id)
    lang = get_lang(user)
    try:
        await cq.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await cq.message.answer(t(lang, "appeal_cancelled"))
    await show_menu(cq.message, user)
    await cq.answer()


@router.callback_query(NewAppeal.category, F.data.startswith("cat:"))
async def new_appeal_category(cq: CallbackQuery, state: FSMContext):
    category = cq.data.split(":", 1)[1]
    await state.update_data(category=category)
    user = await db.get_user(cq.from_user.id)
    lang = get_lang(user)
    try:
        await cq.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await state.set_state(NewAppeal.text)
    await cq.message.answer(t(lang, "enter_appeal_text"), reply_markup=kb.cancel_kb(lang))
    await cq.answer()


@router.message(NewAppeal.text, F.text)
async def new_appeal_text(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    lang = get_lang(user)
    await state.update_data(text=message.text)
    await state.set_state(NewAppeal.media)
    await message.answer(t(lang, "ask_media"), reply_markup=kb.skip_cancel_kb(lang))


@router.message(NewAppeal.media, F.text.in_(all_texts("btn_skip")))
async def new_appeal_skip(message: Message, state: FSMContext):
    await _show_confirm(message, state, None, None)


@router.message(NewAppeal.media, F.photo)
async def new_appeal_photo(message: Message, state: FSMContext):
    await _show_confirm(message, state, message.photo[-1].file_id, "photo")


@router.message(NewAppeal.media, F.document)
async def new_appeal_document(message: Message, state: FSMContext):
    await _show_confirm(message, state, message.document.file_id, "document")


@router.message(NewAppeal.media)
async def new_appeal_media_wrong(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    lang = get_lang(user)
    await message.answer(t(lang, "media_wrong_type"))


async def _show_confirm(message: Message, state: FSMContext, file_id, file_type):
    user = await db.get_user(message.from_user.id)
    lang = get_lang(user)
    await state.update_data(file_id=file_id, file_type=file_type)
    data = await state.get_data()
    await state.set_state(NewAppeal.confirm)
    text = t(
        lang, "confirm_appeal",
        category=t(lang, data["category"]),
        text=esc(data["text"]),
    )
    await message.answer(text, reply_markup=kb.confirm_cancel_kb(lang))


@router.message(NewAppeal.confirm, F.text.in_(all_texts("btn_confirm")))
async def new_appeal_confirm(message: Message, state: FSMContext):
    data = await state.get_data()
    uid = message.from_user.id
    user = await db.get_user(uid)
    lang = get_lang(user)

    appeal_id = await db.create_appeal(
        user_id=uid,
        category=data["category"],
        text=data["text"],
        file_id=data.get("file_id"),
        file_type=data.get("file_type"),
    )
    await state.clear()
    await message.answer(
        t(lang, "appeal_created", number=appeal_id),
        reply_markup=kb.main_menu_kb(lang),
    )
    await notify_new_appeal(message.bot, appeal_id)


# ---------------------------------------------------------------------------
# Mening murojaatlarim
# ---------------------------------------------------------------------------
@router.message(F.text.in_(all_texts("btn_my_appeals")))
async def my_appeals(message: Message, state: FSMContext):
    await state.clear()
    uid = message.from_user.id
    user = await db.get_user(uid)
    lang = get_lang(user)
    appeals = await db.get_user_appeals(uid)
    if not appeals:
        await message.answer(t(lang, "no_appeals"))
        return

    parts = [t(lang, "my_appeals_title")]
    for a in appeals[:20]:
        parts.append("")
        parts.append(t(
            lang, "appeal_short",
            number=a["id"],
            category=t(lang, a["category"]),
            status=status_text(lang, a["status"]),
            date=fmt_date(a["created_at"]),
        ))
    await message.answer("\n".join(parts))


# ---------------------------------------------------------------------------
# Murojaat holati (ariza raqami bo'yicha)
# ---------------------------------------------------------------------------
@router.message(F.text.in_(all_texts("btn_check_status")))
async def check_status_start(message: Message, state: FSMContext):
    await state.clear()
    user = await db.get_user(message.from_user.id)
    lang = get_lang(user)
    await state.set_state(CheckStatus.tracking)
    await message.answer(t(lang, "enter_tracking"), reply_markup=kb.cancel_kb(lang))


@router.message(CheckStatus.tracking, F.text)
async def check_status_result(message: Message, state: FSMContext):
    uid = message.from_user.id
    user = await db.get_user(uid)
    lang = get_lang(user)

    digits = "".join(ch for ch in message.text if ch.isdigit())
    appeal = await db.get_appeal(int(digits)) if digits else None

    # Fuqaro faqat o'z murojaatini ko'ra oladi
    if not appeal or appeal["user_id"] != uid:
        await message.answer(t(lang, "appeal_not_found"))
        return

    await state.clear()
    text = t(
        lang, "appeal_detail_citizen",
        number=appeal["id"],
        category=t(lang, appeal["category"]),
        status=status_text(lang, appeal["status"]),
        date=fmt_date(appeal["created_at"]),
        text=esc(appeal["text"]),
    )
    responses = await db.get_responses(appeal["id"])
    if responses:
        text += t(lang, "responses_title")
        for r in responses:
            text += t(lang, "response_item", text=esc(r["text"]), date=fmt_date(r["created_at"]))
    else:
        text += t(lang, "no_response_yet")

    await message.answer(text, reply_markup=kb.main_menu_kb(lang))
