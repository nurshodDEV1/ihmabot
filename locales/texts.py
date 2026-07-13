"""Ko'p tilli matnlar: o'zbek (lotin), o'zbek (kirill), rus."""

# Til kodlari
LANGUAGES = ["uz_latin", "uz_cyrillic", "ru"]
LANGUAGE_NAMES = {
    "uz_latin": "🇺🇿 O'zbekcha (lotin)",
    "uz_cyrillic": "🇺🇿 Ўзбекча (кирилл)",
    "ru": "🇷🇺 Русский",
}

# Kategoriya kalitlari (bazada shu kalit saqlanadi, ko'rsatishda tarjima qilinadi)
CATEGORIES = [
    "cat_benefits",
    "cat_disability",
    "cat_elderly",
    "cat_children",
    "cat_material",
    "cat_other",
]

TEXTS: dict[str, dict[str, str]] = {
    # =====================================================================
    "uz_latin": {
        # Ro'yxatdan o'tish / start
        "choose_language": "Iltimos, tilni tanlang:",
        "ask_phone": "Ro'yxatdan o'tish uchun telefon raqamingizni yuboring.\n\nPastdagi tugmani bosing 👇",
        "btn_share_phone": "📱 Telefon raqamni yuborish",
        "ask_fullname": "👤 Iltimos, familiya, ism va otangizning ismini to'liq yozing.\n\nMasalan: <b>Aliyev Vali Akmalovich</b>",
        "welcome": "Assalomu alaykum, <b>{name}</b>!\n\n<b>Inson ijtimoiy xizmatlari markazi</b> murojaatlar botiga xush kelibsiz.\n\nQuyidagi menyudan kerakli bo'limni tanlang.",
        "main_menu": "🏠 Asosiy menyu. Kerakli bo'limni tanlang:",

        # Fuqaro menyusi
        "btn_new_appeal": "📝 Yangi murojaat",
        "btn_my_appeals": "📋 Mening murojaatlarim",
        "btn_check_status": "🔍 Murojaat holati",
        "btn_language": "🌐 Tilni o'zgartirish",
        "btn_info": "ℹ️ Markaz haqida",

        # Kategoriyalar
        "cat_benefits": "💰 Ijtimoiy nafaqa",
        "cat_disability": "♿ Nogironlik bo'yicha yordam",
        "cat_elderly": "👵 Keksa va yolg'iz insonlar",
        "cat_children": "👶 Bolalar himoyasi",
        "cat_material": "🎁 Moddiy yordam",
        "cat_other": "📌 Boshqa masala",

        # Yangi murojaat jarayoni
        "choose_category": "Murojaat mavzusini (kategoriyani) tanlang:",
        "enter_appeal_text": "✍️ Murojaatingiz matnini to'liq yozing.\n\nMuammoni yoki so'rovingizni aniq bayon qiling.",
        "ask_media": "📎 Agar hujjat yoki rasm ilova qilmoqchi bo'lsangiz, yuboring.\n\nAgar shart bo'lmasa, «O'tkazib yuborish» tugmasini bosing.",
        "btn_skip": "⏭ O'tkazib yuborish",
        "confirm_appeal": "Murojaatingizni tasdiqlang:\n\n🗂 <b>Kategoriya:</b> {category}\n📄 <b>Matn:</b>\n{text}\n\nHammasi to'g'rimi?",
        "btn_confirm": "✅ Tasdiqlash va yuborish",
        "btn_cancel": "❌ Bekor qilish",
        "appeal_created": "✅ Murojaatingiz qabul qilindi!\n\n🆔 Ariza raqamingiz: <b>№{number}</b>\n\nUshbu raqam orqali murojaat holatini kuzatib borishingiz mumkin. Mutaxassislarimiz tez orada javob berishadi.",
        "appeal_cancelled": "❌ Murojaat bekor qilindi.",
        "media_wrong_type": "⚠️ Iltimos, rasm yoki hujjat yuboring, yoki «O'tkazib yuborish» tugmasini bosing.",

        # Mening murojaatlarim
        "my_appeals_title": "📋 <b>Sizning murojaatlaringiz:</b>",
        "no_appeals": "Sizda hali murojaatlar yo'q.",
        "appeal_short": "🆔 <b>№{number}</b> — {category}\n📊 Holat: {status}\n📅 {date}",

        # Holatni tekshirish
        "enter_tracking": "🔍 Ariza raqamini kiriting (masalan: 12):",
        "appeal_not_found": "❌ Bunday raqamli murojaat topilmadi. Raqamni tekshirib qayta kiriting.",
        "appeal_detail_citizen": "🆔 <b>Murojaat №{number}</b>\n\n🗂 Kategoriya: {category}\n📊 Holat: {status}\n📅 Yuborilgan: {date}\n\n📄 <b>Matningiz:</b>\n{text}",
        "responses_title": "\n\n💬 <b>Javoblar:</b>",
        "response_item": "\n— {text}\n  <i>({date})</i>",
        "no_response_yet": "\n\n⏳ Hozircha javob berilmagan.",

        # Status nomlari
        "status_new": "🆕 Yangi",
        "status_in_progress": "🔧 Ko'rib chiqilmoqda",
        "status_answered": "✅ Javob berilgan",
        "status_closed": "🔒 Yopilgan",

        # Til / Ma'lumot
        "language_changed": "✅ Til o'zgartirildi.",
        "info_text": "ℹ️ <b>Inson ijtimoiy xizmatlari markazi</b>\n\nMarkaz aholining ijtimoiy himoyaga muhtoj qatlamlariga — nafaqa, moddiy yordam, nogironligi bo'lgan shaxslar, keksalar va bolalarga xizmat ko'rsatadi.\n\nUshbu bot orqali murojaat yo'llashingiz va uning holatini kuzatishingiz mumkin.\n\n☎️ Ishonch telefoni: 1234",

        # Umumiy
        "back": "◀️ Orqaga",
        "not_registered": "Iltimos, avval /start buyrug'i orqali ro'yxatdan o'ting.",
        "unknown": "Tushunmadim. Iltimos, menyudagi tugmalardan foydalaning.",

        # === Operator tomoni ===
        "operator_menu": "👨‍💼 <b>Operator paneli</b>. Bo'limni tanlang:",
        "btn_new_appeals": "🆕 Yangi murojaatlar",
        "btn_my_work": "🗂 Ko'rib chiqilayotganlar",
        "op_no_new": "Yangi murojaatlar yo'q. 👍",
        "op_no_work": "Ko'rib chiqilayotgan murojaatlaringiz yo'q.",
        "op_appeal_detail": "🆔 <b>Murojaat №{number}</b>\n\n👤 F.I.Sh: {name}\n💬 Telegram: {tg}\n📞 Telefon: {phone}\n🗂 Kategoriya: {category}\n📊 Holat: {status}\n📅 Sana: {date}\n\n📄 <b>Matn:</b>\n{text}",
        "btn_take": "👀 Ko'rib chiqishga olish",
        "btn_reply": "💬 Javob berish",
        "btn_close": "🔒 Yopish",
        "op_enter_reply": "✍️ Fuqaroga yuboriladigan javob matnini yozing (№{number}):",
        "op_reply_sent": "✅ Javob fuqaroga yuborildi.",
        "op_taken": "✅ Murojaat ko'rib chiqishga olindi. Endi u «Ko'rib chiqilayotganlar» bo'limida.",
        "op_closed": "🔒 Murojaat yopildi.",
        "op_already_taken": "⚠️ Bu murojaatni allaqachon boshqa operator ({name}) ishga olgan.",

        # === Admin tomoni ===
        "admin_menu": "🛠 <b>Administrator paneli</b>:",
        "btn_stats": "📊 Statistika",
        "btn_operators": "👥 Operatorlar",
        "stats_text": "📊 <b>Statistika</b>\n\n📥 Jami murojaatlar: {total}\n📅 Bugun: {today}\n\n🆕 Yangi: {new}\n🔧 Ko'rib chiqilmoqda: {in_progress}\n✅ Javob berilgan: {answered}\n🔒 Yopilgan: {closed}\n\n👥 Fuqarolar: {citizens}\n👨‍💼 Operatorlar: {operators}",
        "operators_title": "👥 <b>Operatorlar ro'yxati:</b>",
        "no_operators": "Hali operatorlar qo'shilmagan.",
        "operator_item": "• {name} (ID: <code>{id}</code>)",
        "btn_add_operator": "➕ Operator qo'shish",
        "btn_remove_operator": "➖ Operatorni o'chirish",
        "enter_operator_id": "Yangi operatorning Telegram ID raqamini yuboring.\n\n(Foydalanuvchi ID sini @userinfobot orqali bilib olish mumkin.)",
        "enter_remove_operator_id": "O'chiriladigan operatorning ID raqamini yuboring:",
        "operator_added": "✅ Foydalanuvchi operator etib tayinlandi (ID: {id}).",
        "operator_removed": "✅ Operator o'chirildi (ID: {id}).",
        "invalid_id": "⚠️ Noto'g'ri ID. Faqat raqam yuboring.",
        "not_an_operator": "⚠️ Bu ID operator emas.",

        # Bildirishnomalar
        "notify_new_appeal": "🔔 <b>Yangi murojaat!</b>\n\n🆔 №{number}\n🗂 {category}\n👤 {name}\n\n📄 {text}",
        "notify_reply": "💬 <b>Murojaatingizga javob keldi!</b>\n\n🆔 №{number}\n\n{text}",
        "notify_status_closed": "🔒 Sizning №{number} raqamli murojaatingiz yopildi. Rahmat!",
    },

    # =====================================================================
    "uz_cyrillic": {
        "choose_language": "Илтимос, тилни танланг:",
        "ask_phone": "Рўйхатдан ўтиш учун телефон рақамингизни юборинг.\n\nПастдаги тугмани босинг 👇",
        "btn_share_phone": "📱 Телефон рақамни юбориш",
        "ask_fullname": "👤 Илтимос, фамилия, исм ва отангизнинг исмини тўлиқ ёзинг.\n\nМасалан: <b>Алиев Вали Акмалович</b>",
        "welcome": "Ассалому алайкум, <b>{name}</b>!\n\n<b>Инсон ижтимоий хизматлари маркази</b> мурожаатлар ботига хуш келибсиз.\n\nҚуйидаги менюдан керакли бўлимни танланг.",
        "main_menu": "🏠 Асосий меню. Керакли бўлимни танланг:",

        "btn_new_appeal": "📝 Янги мурожаат",
        "btn_my_appeals": "📋 Менинг мурожаатларим",
        "btn_check_status": "🔍 Мурожаат ҳолати",
        "btn_language": "🌐 Тилни ўзгартириш",
        "btn_info": "ℹ️ Марказ ҳақида",

        "cat_benefits": "💰 Ижтимоий нафақа",
        "cat_disability": "♿ Ногиронлик бўйича ёрдам",
        "cat_elderly": "👵 Кекса ва ёлғиз инсонлар",
        "cat_children": "👶 Болалар ҳимояси",
        "cat_material": "🎁 Моддий ёрдам",
        "cat_other": "📌 Бошқа масала",

        "choose_category": "Мурожаат мавзусини (категорияни) танланг:",
        "enter_appeal_text": "✍️ Мурожаатингиз матнини тўлиқ ёзинг.\n\nМуаммони ёки сўровингизни аниқ баён қилинг.",
        "ask_media": "📎 Агар ҳужжат ёки расм илова қилмоқчи бўлсангиз, юборинг.\n\nАгар шарт бўлмаса, «Ўтказиб юбориш» тугмасини босинг.",
        "btn_skip": "⏭ Ўтказиб юбориш",
        "confirm_appeal": "Мурожаатингизни тасдиқланг:\n\n🗂 <b>Категория:</b> {category}\n📄 <b>Матн:</b>\n{text}\n\nҲаммаси тўғрими?",
        "btn_confirm": "✅ Тасдиқлаш ва юбориш",
        "btn_cancel": "❌ Бекор қилиш",
        "appeal_created": "✅ Мурожаатингиз қабул қилинди!\n\n🆔 Ариза рақамингиз: <b>№{number}</b>\n\nУшбу рақам орқали мурожаат ҳолатини кузатиб боришингиз мумкин. Мутахассисларимиз тез орада жавоб беришади.",
        "appeal_cancelled": "❌ Мурожаат бекор қилинди.",
        "media_wrong_type": "⚠️ Илтимос, расм ёки ҳужжат юборинг, ёки «Ўтказиб юбориш» тугмасини босинг.",

        "my_appeals_title": "📋 <b>Сизнинг мурожаатларингиз:</b>",
        "no_appeals": "Сизда ҳали мурожаатлар йўқ.",
        "appeal_short": "🆔 <b>№{number}</b> — {category}\n📊 Ҳолат: {status}\n📅 {date}",

        "enter_tracking": "🔍 Ариза рақамини киритинг (масалан: 12):",
        "appeal_not_found": "❌ Бундай рақамли мурожаат топилмади. Рақамни текшириб қайта киритинг.",
        "appeal_detail_citizen": "🆔 <b>Мурожаат №{number}</b>\n\n🗂 Категория: {category}\n📊 Ҳолат: {status}\n📅 Юборилган: {date}\n\n📄 <b>Матнингиз:</b>\n{text}",
        "responses_title": "\n\n💬 <b>Жавоблар:</b>",
        "response_item": "\n— {text}\n  <i>({date})</i>",
        "no_response_yet": "\n\n⏳ Ҳозирча жавоб берилмаган.",

        "status_new": "🆕 Янги",
        "status_in_progress": "🔧 Кўриб чиқилмоқда",
        "status_answered": "✅ Жавоб берилган",
        "status_closed": "🔒 Ёпилган",

        "language_changed": "✅ Тил ўзгартирилди.",
        "info_text": "ℹ️ <b>Инсон ижтимоий хизматлари маркази</b>\n\nМарказ аҳолининг ижтимоий ҳимояга муҳтож қатламларига — нафақа, моддий ёрдам, ногиронлиги бўлган шахслар, кексалар ва болаларга хизмат кўрсатади.\n\nУшбу бот орқали мурожаат йўллашингиз ва унинг ҳолатини кузатишингиз мумкин.\n\n☎️ Ишонч телефони: 1234",

        "back": "◀️ Орқага",
        "not_registered": "Илтимос, аввал /start буйруғи орқали рўйхатдан ўтинг.",
        "unknown": "Тушунмадим. Илтимос, менюдаги тугмалардан фойдаланинг.",

        "operator_menu": "👨‍💼 <b>Оператор панели</b>. Бўлимни танланг:",
        "btn_new_appeals": "🆕 Янги мурожаатлар",
        "btn_my_work": "🗂 Кўриб чиқилаётганлар",
        "op_no_new": "Янги мурожаатлар йўқ. 👍",
        "op_no_work": "Кўриб чиқилаётган мурожаатларингиз йўқ.",
        "op_appeal_detail": "🆔 <b>Мурожаат №{number}</b>\n\n👤 Ф.И.Ш: {name}\n💬 Телеграм: {tg}\n📞 Телефон: {phone}\n🗂 Категория: {category}\n📊 Ҳолат: {status}\n📅 Сана: {date}\n\n📄 <b>Матн:</b>\n{text}",
        "btn_take": "👀 Кўриб чиқишга олиш",
        "btn_reply": "💬 Жавоб бериш",
        "btn_close": "🔒 Ёпиш",
        "op_enter_reply": "✍️ Фуқарога юбориладиган жавоб матнини ёзинг (№{number}):",
        "op_reply_sent": "✅ Жавоб фуқарога юборилди.",
        "op_taken": "✅ Мурожаат кўриб чиқишга олинди. Энди у «Кўриб чиқилаётганлар» бўлимида.",
        "op_closed": "🔒 Мурожаат ёпилди.",
        "op_already_taken": "⚠️ Бу мурожаатни аллақачон бошқа оператор ({name}) ишга олган.",

        "admin_menu": "🛠 <b>Администратор панели</b>:",
        "btn_stats": "📊 Статистика",
        "btn_operators": "👥 Операторлар",
        "stats_text": "📊 <b>Статистика</b>\n\n📥 Жами мурожаатлар: {total}\n📅 Бугун: {today}\n\n🆕 Янги: {new}\n🔧 Кўриб чиқилмоқда: {in_progress}\n✅ Жавоб берилган: {answered}\n🔒 Ёпилган: {closed}\n\n👥 Фуқаролар: {citizens}\n👨‍💼 Операторлар: {operators}",
        "operators_title": "👥 <b>Операторлар рўйхати:</b>",
        "no_operators": "Ҳали операторлар қўшилмаган.",
        "operator_item": "• {name} (ID: <code>{id}</code>)",
        "btn_add_operator": "➕ Оператор қўшиш",
        "btn_remove_operator": "➖ Операторни ўчириш",
        "enter_operator_id": "Янги операторнинг Telegram ID рақамини юборинг.\n\n(Фойдаланувчи ID сини @userinfobot орқали билиб олиш мумкин.)",
        "enter_remove_operator_id": "Ўчириладиган операторнинг ID рақамини юборинг:",
        "operator_added": "✅ Фойдаланувчи оператор этиб тайинланди (ID: {id}).",
        "operator_removed": "✅ Оператор ўчирилди (ID: {id}).",
        "invalid_id": "⚠️ Нотўғри ID. Фақат рақам юборинг.",
        "not_an_operator": "⚠️ Бу ID оператор эмас.",

        "notify_new_appeal": "🔔 <b>Янги мурожаат!</b>\n\n🆔 №{number}\n🗂 {category}\n👤 {name}\n\n📄 {text}",
        "notify_reply": "💬 <b>Мурожаатингизга жавоб келди!</b>\n\n🆔 №{number}\n\n{text}",
        "notify_status_closed": "🔒 Сизнинг №{number} рақамли мурожаатингиз ёпилди. Раҳмат!",
    },

    # =====================================================================
    "ru": {
        "choose_language": "Пожалуйста, выберите язык:",
        "ask_phone": "Для регистрации отправьте свой номер телефона.\n\nНажмите кнопку ниже 👇",
        "btn_share_phone": "📱 Отправить номер телефона",
        "ask_fullname": "👤 Пожалуйста, напишите свою фамилию, имя и отчество полностью.\n\nНапример: <b>Алиев Вали Акмалович</b>",
        "welcome": "Здравствуйте, <b>{name}</b>!\n\nДобро пожаловать в бот обращений <b>Центра социального обслуживания населения</b>.\n\nВыберите нужный раздел из меню ниже.",
        "main_menu": "🏠 Главное меню. Выберите раздел:",

        "btn_new_appeal": "📝 Новое обращение",
        "btn_my_appeals": "📋 Мои обращения",
        "btn_check_status": "🔍 Статус обращения",
        "btn_language": "🌐 Сменить язык",
        "btn_info": "ℹ️ О центре",

        "cat_benefits": "💰 Социальные пособия",
        "cat_disability": "♿ Помощь по инвалидности",
        "cat_elderly": "👵 Пожилые и одинокие",
        "cat_children": "👶 Защита детей",
        "cat_material": "🎁 Материальная помощь",
        "cat_other": "📌 Другой вопрос",

        "choose_category": "Выберите тему (категорию) обращения:",
        "enter_appeal_text": "✍️ Напишите текст вашего обращения полностью.\n\nЧётко изложите проблему или запрос.",
        "ask_media": "📎 Если хотите приложить документ или фото — отправьте его.\n\nЕсли не нужно, нажмите «Пропустить».",
        "btn_skip": "⏭ Пропустить",
        "confirm_appeal": "Подтвердите обращение:\n\n🗂 <b>Категория:</b> {category}\n📄 <b>Текст:</b>\n{text}\n\nВсё верно?",
        "btn_confirm": "✅ Подтвердить и отправить",
        "btn_cancel": "❌ Отменить",
        "appeal_created": "✅ Ваше обращение принято!\n\n🆔 Номер заявки: <b>№{number}</b>\n\nПо этому номеру вы можете отслеживать статус обращения. Наши специалисты скоро ответят.",
        "appeal_cancelled": "❌ Обращение отменено.",
        "media_wrong_type": "⚠️ Пожалуйста, отправьте фото или документ, либо нажмите «Пропустить».",

        "my_appeals_title": "📋 <b>Ваши обращения:</b>",
        "no_appeals": "У вас пока нет обращений.",
        "appeal_short": "🆔 <b>№{number}</b> — {category}\n📊 Статус: {status}\n📅 {date}",

        "enter_tracking": "🔍 Введите номер заявки (например: 12):",
        "appeal_not_found": "❌ Обращение с таким номером не найдено. Проверьте номер и попробуйте снова.",
        "appeal_detail_citizen": "🆔 <b>Обращение №{number}</b>\n\n🗂 Категория: {category}\n📊 Статус: {status}\n📅 Отправлено: {date}\n\n📄 <b>Ваш текст:</b>\n{text}",
        "responses_title": "\n\n💬 <b>Ответы:</b>",
        "response_item": "\n— {text}\n  <i>({date})</i>",
        "no_response_yet": "\n\n⏳ Ответа пока нет.",

        "status_new": "🆕 Новое",
        "status_in_progress": "🔧 На рассмотрении",
        "status_answered": "✅ Отвечено",
        "status_closed": "🔒 Закрыто",

        "language_changed": "✅ Язык изменён.",
        "info_text": "ℹ️ <b>Центр социального обслуживания населения</b>\n\nЦентр обслуживает социально уязвимые слои населения — по вопросам пособий, материальной помощи, лиц с инвалидностью, пожилых и детей.\n\nЧерез этот бот вы можете отправить обращение и отслеживать его статус.\n\n☎️ Телефон доверия: 1234",

        "back": "◀️ Назад",
        "not_registered": "Пожалуйста, сначала зарегистрируйтесь через команду /start.",
        "unknown": "Не понял. Пожалуйста, используйте кнопки меню.",

        "operator_menu": "👨‍💼 <b>Панель оператора</b>. Выберите раздел:",
        "btn_new_appeals": "🆕 Новые обращения",
        "btn_my_work": "🗂 На рассмотрении",
        "op_no_new": "Новых обращений нет. 👍",
        "op_no_work": "У вас нет обращений на рассмотрении.",
        "op_appeal_detail": "🆔 <b>Обращение №{number}</b>\n\n👤 Ф.И.О: {name}\n💬 Телеграм: {tg}\n📞 Телефон: {phone}\n🗂 Категория: {category}\n📊 Статус: {status}\n📅 Дата: {date}\n\n📄 <b>Текст:</b>\n{text}",
        "btn_take": "👀 Взять на рассмотрение",
        "btn_reply": "💬 Ответить",
        "btn_close": "🔒 Закрыть",
        "op_enter_reply": "✍️ Напишите текст ответа гражданину (№{number}):",
        "op_reply_sent": "✅ Ответ отправлен гражданину.",
        "op_taken": "✅ Обращение взято на рассмотрение. Теперь оно в разделе «На рассмотрении».",
        "op_closed": "🔒 Обращение закрыто.",
        "op_already_taken": "⚠️ Это обращение уже взял в работу другой оператор ({name}).",

        "admin_menu": "🛠 <b>Панель администратора</b>:",
        "btn_stats": "📊 Статистика",
        "btn_operators": "👥 Операторы",
        "stats_text": "📊 <b>Статистика</b>\n\n📥 Всего обращений: {total}\n📅 Сегодня: {today}\n\n🆕 Новые: {new}\n🔧 На рассмотрении: {in_progress}\n✅ Отвечено: {answered}\n🔒 Закрыто: {closed}\n\n👥 Граждане: {citizens}\n👨‍💼 Операторы: {operators}",
        "operators_title": "👥 <b>Список операторов:</b>",
        "no_operators": "Операторы ещё не добавлены.",
        "operator_item": "• {name} (ID: <code>{id}</code>)",
        "btn_add_operator": "➕ Добавить оператора",
        "btn_remove_operator": "➖ Удалить оператора",
        "enter_operator_id": "Отправьте Telegram ID нового оператора.\n\n(ID пользователя можно узнать через @userinfobot.)",
        "enter_remove_operator_id": "Отправьте ID оператора для удаления:",
        "operator_added": "✅ Пользователь назначен оператором (ID: {id}).",
        "operator_removed": "✅ Оператор удалён (ID: {id}).",
        "invalid_id": "⚠️ Неверный ID. Отправьте только число.",
        "not_an_operator": "⚠️ Этот ID не является оператором.",

        "notify_new_appeal": "🔔 <b>Новое обращение!</b>\n\n🆔 №{number}\n🗂 {category}\n👤 {name}\n\n📄 {text}",
        "notify_reply": "💬 <b>На ваше обращение поступил ответ!</b>\n\n🆔 №{number}\n\n{text}",
        "notify_status_closed": "🔒 Ваше обращение №{number} закрыто. Спасибо!",
    },
}

DEFAULT_LANG = "uz_latin"


def t(lang: str | None, key: str, **kwargs) -> str:
    """Kalit bo'yicha matnni tanlangan tilda qaytaradi."""
    lang = lang if lang in TEXTS else DEFAULT_LANG
    text = TEXTS[lang].get(key) or TEXTS[DEFAULT_LANG].get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text


def all_texts(key: str) -> set[str]:
    """Tugma matnining barcha tildagi variantlari (F.text.in_ uchun)."""
    return {TEXTS[lang][key] for lang in TEXTS if key in TEXTS[lang]}
