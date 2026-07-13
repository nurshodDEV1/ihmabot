# Inson ijtimoiy xizmatlari markazi — Murojaatlar boti

Fuqarolarning murojaatlarini qabul qilish va ular bilan ishlash uchun Telegram bot.
Fuqaro murojaat yuboradi → ariza raqami oladi → operatorlar ko'rib chiqib javob beradi →
murojaat holati kuzatiladi.

## Imkoniyatlar

**Fuqaro uchun:**
- 📝 Yangi murojaat yuborish (kategoriya, matn, rasm/hujjat ilova qilish)
- 🆔 Har bir murojaatga avtomatik ariza raqami
- 📋 O'z murojaatlari ro'yxati
- 🔍 Ariza raqami bo'yicha holatni tekshirish va javobni ko'rish
- 🌐 3 til: o'zbekcha (lotin), ўзбекча (кирилл), русский

**Operator uchun:**
- 🆕 Yangi murojaatlar bilan tanishish (avtomatik bildirishnoma)
- ✋ Murojaatni ishga olish
- 💬 Fuqaroga javob yuborish
- 🔒 Murojaatni yopish

**Admin uchun:**
- 📊 Statistika (jami, bugungi, statuslar bo'yicha)
- 👥 Operatorlarni qo'shish/o'chirish
- Operatorlarning barcha imkoniyatlari

## Murojaat statuslari
`Yangi` → `Ko'rib chiqilmoqda` → `Javob berilgan` → `Yopilgan`

## O'rnatish

1. **Python 3.10+** o'rnatilgan bo'lishi kerak.

2. Kutubxonalarni o'rnating:
   ```powershell
   pip install -r requirements.txt
   ```

3. `.env` faylini sozlang (`.env.example` dan nusxa oling):
   ```
   BOT_TOKEN=@BotFather_dan_olingan_token
   ADMIN_IDS=sizning_telegram_id
   DB_PATH=database.db
   ```
   - **BOT_TOKEN** — [@BotFather](https://t.me/BotFather) da yangi bot yaratib oling.
   - **ADMIN_IDS** — o'z Telegram ID raqamingiz ([@userinfobot](https://t.me/userinfobot) orqali biling).
     Bir nechta admin bo'lsa vergul bilan ajrating: `111,222`.

4. Botni ishga tushiring:
   ```powershell
   python bot.py
   ```

## Foydalanish

1. Botga `/start` yuboring.
2. Admin sifatida siz avtomatik admin panelini ko'rasiz — u yerdan operatorlarni qo'shing.
3. Oddiy foydalanuvchi til va telefon raqamini kiritib, murojaat yuborishi mumkin.

## Loyiha tuzilmasi

```
├── bot.py              # Ishga tushirish nuqtasi
├── config.py           # .env dan sozlamalar
├── states.py           # FSM holatlari
├── keyboards.py        # Reply va inline klaviaturalar
├── utils.py            # Yordamchi funksiyalar, bildirishnomalar
├── filters.py          # Rolga asoslangan filtrlar
├── database/
│   └── db.py           # SQLite bilan ishlash
├── locales/
│   └── texts.py        # 3 tilli matnlar
└── handlers/
    ├── common.py       # /start, ro'yxatdan o'tish, til
    ├── citizen.py      # Fuqaro handlerlari
    ├── operator.py     # Operator handlerlari
    ├── admin.py        # Admin handlerlari
    └── fallback.py     # Tushunarsiz xabarlar
```

## Texnologiyalar
- [aiogram 3.x](https://docs.aiogram.dev/) — Telegram Bot API framework
- SQLite (aiosqlite) — ma'lumotlar bazasi
- python-dotenv — muhit sozlamalari
