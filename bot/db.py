import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "bot.db"


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    with _conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                tg_id       INTEGER PRIMARY KEY,
                username    TEXT,
                marzban_username TEXT UNIQUE,
                role        TEXT DEFAULT 'trial',
                created_at  TEXT DEFAULT (datetime('now')),
                expires_at  TEXT,
                trial_used  INTEGER DEFAULT 0
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id           INTEGER,
                amount          REAL,
                currency        TEXT,
                method          TEXT,
                status          TEXT DEFAULT 'pending',
                created_at      TEXT DEFAULT (datetime('now')),
                payload         TEXT,
                external_id     TEXT UNIQUE,
                plan            TEXT,
                email           TEXT
            )
        """)
        # Migrate legacy tables
        cols = {row[1] for row in c.execute("PRAGMA table_info(payments)").fetchall()}
        for col, decl in [
            ("external_id", "TEXT"),
            ("plan", "TEXT"),
            ("email", "TEXT"),
        ]:
            if col not in cols:
                c.execute(f"ALTER TABLE payments ADD COLUMN {col} {decl}")

        c.execute("""
            CREATE TABLE IF NOT EXISTS invites (
                code         TEXT PRIMARY KEY,
                max_uses     INTEGER DEFAULT 1,
                uses_count   INTEGER DEFAULT 0,
                created_by   INTEGER,
                created_at   TEXT DEFAULT (datetime('now')),
                note         TEXT
            )
        """)


def get_user(tg_id: int) -> dict | None:
    with _conn() as c:
        row = c.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,)).fetchone()
        return dict(row) if row else None


def create_user(tg_id: int, username: str | None, marzban_username: str,
                role: str, expires_at: str) -> dict:
    with _conn() as c:
        c.execute("""
            INSERT INTO users (tg_id, username, marzban_username, role, expires_at, trial_used)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tg_id, username, marzban_username, role, expires_at,
              1 if role == "trial" else 0))
    return get_user(tg_id)


def update_user(tg_id: int, **kwargs):
    allowed = {"role", "expires_at", "trial_used", "marzban_username", "username"}
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [tg_id]
    with _conn() as c:
        c.execute(f"UPDATE users SET {set_clause} WHERE tg_id = ?", values)


def get_all_users() -> list[dict]:
    with _conn() as c:
        rows = c.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]


def get_active_users_count() -> int:
    now = datetime.utcnow().isoformat()
    with _conn() as c:
        row = c.execute(
            "SELECT COUNT(*) as cnt FROM users "
            "WHERE expires_at IS NULL OR expires_at > ?",
            (now,),
        ).fetchone()
        return row["cnt"]


def add_payment(tg_id: int, amount: float, currency: str,
                method: str, plan: str, email: str,
                external_id: str, payload: str = "") -> int:
    with _conn() as c:
        cur = c.execute("""
            INSERT INTO payments (tg_id, amount, currency, method, plan, email, external_id, payload)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (tg_id, amount, currency, method, plan, email, external_id, payload))
        return cur.lastrowid


def update_payment(payment_id: int, status: str):
    with _conn() as c:
        c.execute("UPDATE payments SET status = ? WHERE id = ?", (status, payment_id))


def update_payment_by_external(external_id: str, status: str):
    with _conn() as c:
        c.execute(
            "UPDATE payments SET status = ? WHERE external_id = ?",
            (status, external_id),
        )


def create_invite(code: str, max_uses: int, created_by: int, note: str = "") -> None:
    with _conn() as c:
        c.execute(
            "INSERT INTO invites (code, max_uses, created_by, note) VALUES (?, ?, ?, ?)",
            (code, max_uses, created_by, note),
        )


def get_invite(code: str) -> dict | None:
    with _conn() as c:
        row = c.execute("SELECT * FROM invites WHERE code = ?", (code,)).fetchone()
        return dict(row) if row else None


def increment_invite_use(code: str) -> None:
    with _conn() as c:
        c.execute(
            "UPDATE invites SET uses_count = uses_count + 1 WHERE code = ?", (code,)
        )


def get_all_invites() -> list[dict]:
    with _conn() as c:
        rows = c.execute(
            "SELECT * FROM invites ORDER BY created_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def get_email(tg_id: int) -> str | None:
    with _conn() as c:
        row = c.execute(
            "SELECT email FROM payments WHERE tg_id = ? AND email IS NOT NULL "
            "ORDER BY id DESC LIMIT 1", (tg_id,)
        ).fetchone()
        return row["email"] if row else None
