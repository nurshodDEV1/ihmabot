"""SQLite ma'lumotlar bazasi bilan ishlash (aiosqlite orqali)."""
import aiosqlite

from config import config

DB_PATH = config.db_path

# Murojaat statuslari
STATUS_NEW = "new"            # Yangi
STATUS_IN_PROGRESS = "in_progress"  # Ko'rib chiqilmoqda
STATUS_ANSWERED = "answered"  # Javob berilgan
STATUS_CLOSED = "closed"      # Yopilgan

# Rollar
ROLE_CITIZEN = "citizen"
ROLE_OPERATOR = "operator"
ROLE_ADMIN = "admin"


async def init_db() -> None:
    """Jadvallarni yaratadi va adminlarni ro'yxatga qo'shadi."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA foreign_keys = ON")

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                full_name   TEXT,
                fio         TEXT,
                username    TEXT,
                phone       TEXT,
                language    TEXT    DEFAULT 'uz_latin',
                role        TEXT    DEFAULT 'citizen',
                created_at  TEXT    DEFAULT (datetime('now', 'localtime'))
            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS appeals (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                category    TEXT,
                text        TEXT,
                file_id     TEXT,
                file_type   TEXT,
                status      TEXT    DEFAULT 'new',
                operator_id INTEGER,
                created_at  TEXT    DEFAULT (datetime('now', 'localtime')),
                updated_at  TEXT    DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS responses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                appeal_id   INTEGER NOT NULL,
                operator_id INTEGER,
                text        TEXT,
                created_at  TEXT    DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (appeal_id) REFERENCES appeals(id)
            )
            """
        )

        # Migratsiya: eski bazaga 'fio' ustunini qo'shish (agar yo'q bo'lsa)
        cur = await db.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in await cur.fetchall()]
        if "fio" not in columns:
            await db.execute("ALTER TABLE users ADD COLUMN fio TEXT")

        # Adminlarni bootstrap qilish
        for admin_id in config.admin_ids:
            await db.execute(
                "INSERT OR IGNORE INTO users (user_id, role) VALUES (?, ?)",
                (admin_id, ROLE_ADMIN),
            )
            await db.execute(
                "UPDATE users SET role = ? WHERE user_id = ?",
                (ROLE_ADMIN, admin_id),
            )

        await db.commit()


# ---------------------------------------------------------------------------
# Foydalanuvchilar
# ---------------------------------------------------------------------------
async def add_user(user_id: int, full_name: str, username: str | None) -> None:
    """Foydalanuvchini qo'shadi yoki ismini yangilaydi (rol/til saqlanadi)."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO users (user_id, full_name, username)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                full_name = excluded.full_name,
                username  = excluded.username
            """,
            (user_id, full_name, username),
        )
        await db.commit()


async def get_user(user_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = await cur.fetchone()
        return dict(row) if row else None


async def update_language(user_id: int, language: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET language = ? WHERE user_id = ?", (language, user_id)
        )
        await db.commit()


async def update_phone(user_id: int, phone: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET phone = ? WHERE user_id = ?", (phone, user_id)
        )
        await db.commit()


async def update_fio(user_id: int, fio: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET fio = ? WHERE user_id = ?", (fio, user_id)
        )
        await db.commit()


async def set_role(user_id: int, role: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO users (user_id, role) VALUES (?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET role = excluded.role",
            (user_id, role),
        )
        await db.commit()


async def get_operators() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM users WHERE role = ? ORDER BY user_id", (ROLE_OPERATOR,)
        )
        return [dict(r) for r in await cur.fetchall()]


async def get_staff_ids() -> list[int]:
    """Operator va adminlarning ID lari (xabar yuborish uchun)."""
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT user_id FROM users WHERE role IN (?, ?)",
            (ROLE_OPERATOR, ROLE_ADMIN),
        )
        ids = {row[0] for row in await cur.fetchall()}
    ids.update(config.admin_ids)
    return list(ids)


# ---------------------------------------------------------------------------
# Murojaatlar
# ---------------------------------------------------------------------------
async def create_appeal(
    user_id: int,
    category: str,
    text: str,
    file_id: str | None = None,
    file_type: str | None = None,
) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            """
            INSERT INTO appeals (user_id, category, text, file_id, file_type)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, category, text, file_id, file_type),
        )
        await db.commit()
        return cur.lastrowid


async def get_appeal(appeal_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM appeals WHERE id = ?", (appeal_id,))
        row = await cur.fetchone()
        return dict(row) if row else None


async def get_user_appeals(user_id: int) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM appeals WHERE user_id = ? ORDER BY id DESC", (user_id,)
        )
        return [dict(r) for r in await cur.fetchall()]


async def get_appeals_by_status(status: str, limit: int = 20) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM appeals WHERE status = ? ORDER BY id DESC LIMIT ?",
            (status, limit),
        )
        return [dict(r) for r in await cur.fetchall()]


async def get_operator_appeals(operator_id: int, limit: int = 20) -> list[dict]:
    """Operatorga biriktirilgan, hali yopilmagan murojaatlar."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM appeals WHERE operator_id = ? AND status != ? "
            "ORDER BY id DESC LIMIT ?",
            (operator_id, STATUS_CLOSED, limit),
        )
        return [dict(r) for r in await cur.fetchall()]


async def update_status(appeal_id: int, status: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE appeals SET status = ?, updated_at = datetime('now', 'localtime') "
            "WHERE id = ?",
            (status, appeal_id),
        )
        await db.commit()


async def assign_operator(appeal_id: int, operator_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE appeals SET operator_id = ?, status = ?, "
            "updated_at = datetime('now', 'localtime') WHERE id = ?",
            (operator_id, STATUS_IN_PROGRESS, appeal_id),
        )
        await db.commit()


# ---------------------------------------------------------------------------
# Javoblar
# ---------------------------------------------------------------------------
async def add_response(appeal_id: int, operator_id: int, text: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO responses (appeal_id, operator_id, text) VALUES (?, ?, ?)",
            (appeal_id, operator_id, text),
        )
        await db.execute(
            "UPDATE appeals SET status = ?, updated_at = datetime('now', 'localtime') "
            "WHERE id = ?",
            (STATUS_ANSWERED, appeal_id),
        )
        await db.commit()


async def get_responses(appeal_id: int) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM responses WHERE appeal_id = ? ORDER BY id", (appeal_id,)
        )
        return [dict(r) for r in await cur.fetchall()]


# ---------------------------------------------------------------------------
# Statistika
# ---------------------------------------------------------------------------
async def get_stats() -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        cur = await db.execute("SELECT COUNT(*) AS c FROM appeals")
        total = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT status, COUNT(*) AS c FROM appeals GROUP BY status"
        )
        by_status = {row["status"]: row["c"] for row in await cur.fetchall()}

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM appeals "
            "WHERE date(created_at) = date('now', 'localtime')"
        )
        today = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM users WHERE role = ?", (ROLE_CITIZEN,)
        )
        citizens = (await cur.fetchone())["c"]

        cur = await db.execute(
            "SELECT COUNT(*) AS c FROM users WHERE role = ?", (ROLE_OPERATOR,)
        )
        operators = (await cur.fetchone())["c"]

    return {
        "total": total,
        "today": today,
        "new": by_status.get(STATUS_NEW, 0),
        "in_progress": by_status.get(STATUS_IN_PROGRESS, 0),
        "answered": by_status.get(STATUS_ANSWERED, 0),
        "closed": by_status.get(STATUS_CLOSED, 0),
        "citizens": citizens,
        "operators": operators,
    }
