"""Operator handlerlari: murojaatlarni ko'rish, ishga olish, javob berish, yopish."""
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import keyboards as kb
from database import db
from filters import IsStaff
from locales.texts import t, all_texts
from states import OpReply
from utils import get_lang, show_menu, fmt_date, status_text, esc, citizen_name, citizen_nick

router = Router()
router.message.filter(IsStaff())
router.callback_query.filter(IsStaff())


# ---------------------------------------------------------------------------
# Ro'yxatlar
# ---------------------------------------------------------------------------
@router.message(F.text.in_(all_texts("btn_new_appeals")))
async def new_appeals_list(message: Message, state: FSMContext):
    await state.clear()
    user = await db.get_user(message.from_user.id)
    lang = get_lang(user)
    # Faqat yangi va hali hech kim olmagan murojaatlar
    appeals = await db.get_unassigned_appeals()
    if not appeals:
        await message.answer(t(lang, "op_no_new"))
        return
    await message.answer(
        t(lang, "btn_new_appeals"),
        reply_markup=kb.appeals_list_kb(appeals, lang, "opview"),
    )


@router.message(F.text.in_(all_texts("btn_my_work")))
async def my_work_list(message: Message, state: FSMContext):
    await state.clear()
    uid = message.from_user.id
    user = await db.get_user(uid)
    lang = get_lang(user)
    from utils import get_role
    role = get_role(user)

    # Admin barcha ko'rib chiqilayotgan murojaatlarni ko'radi
    if role == db.ROLE_ADMIN:
        appeals = await db.get_all_in_progress_appeals()
    else:
        # Operator faqat o'zi olgan murojaatlarni ko'radi
        appeals = await db.get_operator_appeals(uid)

    if not appeals:
        await message.answer(t(lang, "op_no_work"))
        return
    await message.answer("🗂", reply_markup=kb.appeals_list_kb(appeals, lang, "opview"))


# ---------------------------------------------------------------------------
# Murojaatni ochish
# ---------------------------------------------------------------------------
@router.callback_query(F.data.startswith("opview:"))
async def open_appeal(cq: CallbackQuery, state: FSMContext):
    await state.clear()
    appeal_id = int(cq.data.split(":", 1)[1])
    user = await db.get_user(cq.from_user.id)
    lang = get_lang(user)
    appeal = await db.get_appeal(appeal_id)
    if not appeal:
        await cq.answer(t(lang, "appeal_not_found"), show_alert=True)
        return
    await _send_appeal(cq.message, appeal, lang)
    await cq.answer()


async def _send_appeal(target: Message, appeal: dict, lang: str):
    citizen = await db.get_user(appeal["user_id"])

    # Operator ma'lumotini olish (agar biriktirilgan bo'lsa)
    operator_info = "—"
    if appeal.get("operator_id"):
        operator = await db.get_user(appeal["operator_id"])
        if operator:
            op_name = operator.get("fio") or operator.get("full_name") or "Operator"
            operator_info = f'{esc(op_name)} (ID: {appeal["operator_id"]})'

    text = t(
        lang, "op_appeal_detail",
        number=appeal["id"],
        name=citizen_name(citizen),
        tg=citizen_nick(citizen),
        phone=esc((citizen or {}).get("phone") or "—"),
        address=esc((citizen or {}).get("address") or "—"),
        category=t(lang, appeal["category"]),
        status=status_text(lang, appeal["status"]),
        date=fmt_date(appeal["created_at"]),
        text=esc(appeal["text"]),
        operator=operator_info,
    )
    markup = kb.appeal_actions_kb(lang, appeal)
    # Ilova (rasm/hujjat) bo'lsa alohida yuboramiz — caption uzunligi cheklovidan qochish uchun
    file_id, file_type = appeal.get("file_id"), appeal.get("file_type")
    try:
        if file_id and file_type == "photo":
            await target.answer_photo(file_id)
        elif file_id and file_type == "document":
            await target.answer_document(file_id)
    except Exception:
        pass
    await target.answer(text, reply_markup=markup)


# ---------------------------------------------------------------------------
# Ishga olish
# ---------------------------------------------------------------------------
@router.callback_query(F.data.startswith("optake:"))
async def take_appeal(cq: CallbackQuery):
    appeal_id = int(cq.data.split(":", 1)[1])
    user = await db.get_user(cq.from_user.id)
    lang = get_lang(user)
    appeal = await db.get_appeal(appeal_id)
    if not appeal:
        await cq.answer(t(lang, "appeal_not_found"), show_alert=True)
        return
    if appeal.get("operator_id") and appeal["operator_id"] != cq.from_user.id:
        other = await db.get_user(appeal["operator_id"])
        await cq.answer(
            t(lang, "op_already_taken", name=(other or {}).get("full_name") or "?"),
            show_alert=True,
        )
        return

    await db.assign_operator(appeal_id, cq.from_user.id)
    appeal = await db.get_appeal(appeal_id)
    try:
        await cq.message.edit_reply_markup(reply_markup=kb.appeal_actions_kb(lang, appeal))
    except Exception:
        pass
    await cq.answer(t(lang, "op_taken"), show_alert=True)


# ---------------------------------------------------------------------------
# Yopish
# ---------------------------------------------------------------------------
@router.callback_query(F.data.startswith("opclose:"))
async def close_appeal(cq: CallbackQuery):
    appeal_id = int(cq.data.split(":", 1)[1])
    user = await db.get_user(cq.from_user.id)
    lang = get_lang(user)
    appeal = await db.get_appeal(appeal_id)
    if not appeal:
        await cq.answer(t(lang, "appeal_not_found"), show_alert=True)
        return

    await db.update_status(appeal_id, db.STATUS_CLOSED)
    appeal = await db.get_appeal(appeal_id)
    try:
        await cq.message.edit_reply_markup(reply_markup=kb.appeal_actions_kb(lang, appeal))
    except Exception:
        pass
    await cq.answer(t(lang, "op_closed"), show_alert=True)

    # Fuqaroga xabar
    citizen = await db.get_user(appeal["user_id"])
    clang = get_lang(citizen)
    try:
        await cq.bot.send_message(
            appeal["user_id"], t(clang, "notify_status_closed", number=appeal_id)
        )
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Javob berish
# ---------------------------------------------------------------------------
@router.callback_query(F.data.startswith("opreply:"))
async def reply_start(cq: CallbackQuery, state: FSMContext):
    appeal_id = int(cq.data.split(":", 1)[1])
    user = await db.get_user(cq.from_user.id)
    lang = get_lang(user)
    appeal = await db.get_appeal(appeal_id)
    if not appeal:
        await cq.answer(t(lang, "appeal_not_found"), show_alert=True)
        return
    await state.set_state(OpReply.text)
    await state.update_data(appeal_id=appeal_id)
    await cq.message.answer(
        t(lang, "op_enter_reply", number=appeal_id), reply_markup=kb.cancel_kb(lang)
    )
    await cq.answer()


@router.message(OpReply.text, F.text)
async def reply_send(message: Message, state: FSMContext):
    data = await state.get_data()
    appeal_id = data.get("appeal_id")
    uid = message.from_user.id
    user = await db.get_user(uid)
    lang = get_lang(user)

    appeal = await db.get_appeal(appeal_id)
    if not appeal:
        await state.clear()
        await message.answer(t(lang, "appeal_not_found"))
        await show_menu(message, user)
        return

    # Biriktirilmagan bo'lsa — javob beruvchini biriktiramiz
    if not appeal.get("operator_id"):
        await db.assign_operator(appeal_id, uid)
    await db.add_response(appeal_id, uid, message.text)

    await state.clear()
    await message.answer(t(lang, "op_reply_sent"))
    await show_menu(message, user)

    # Fuqaroga javobni yuboramiz (feedback tugmalari bilan)
    citizen = await db.get_user(appeal["user_id"])
    clang = get_lang(citizen)
    try:
        await message.bot.send_message(
            appeal["user_id"],
            t(clang, "notify_reply", number=appeal_id, text=esc(message.text)),
            reply_markup=kb.feedback_kb(clang, appeal_id),
        )
    except Exception:
        pass
