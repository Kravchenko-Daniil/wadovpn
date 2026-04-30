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
            CREATE TABLE IF NOT EXISTS invites (
                code         TEXT PRIMARY KEY,
                max_uses     INTEGER DEFAULT 1,
                uses_count   INTEGER DEFAULT 0,
                created_by   INTEGER,
                created_at   TEXT DEFAULT (datetime('now')),
                note         TEXT,
                grant_days   INTEGER
            )
        """)
        inv_cols = {row[1] for row in c.execute("PRAGMA table_info(invites)").fetchall()}
        if "grant_days" not in inv_cols:
            c.execute("ALTER TABLE invites ADD COLUMN grant_days INTEGER")

        c.execute("""
            CREATE TABLE IF NOT EXISTS whitelist (
                username    TEXT PRIMARY KEY,
                added_by    INTEGER,
                added_at    TEXT DEFAULT (datetime('now'))
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


def create_invite(code: str, max_uses: int, created_by: int, note: str = "",
                  grant_days: int | None = None) -> None:
    with _conn() as c:
        c.execute(
            "INSERT INTO invites (code, max_uses, created_by, note, grant_days) "
            "VALUES (?, ?, ?, ?, ?)",
            (code, max_uses, created_by, note, grant_days),
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


def add_whitelist(username: str, added_by: int) -> bool:
    with _conn() as c:
        try:
            c.execute(
                "INSERT INTO whitelist (username, added_by) VALUES (?, ?)",
                (username.lower(), added_by),
            )
            return True
        except sqlite3.IntegrityError:
            return False


def remove_whitelist(username: str) -> bool:
    with _conn() as c:
        cur = c.execute(
            "DELETE FROM whitelist WHERE username = ?", (username.lower(),)
        )
        return cur.rowcount > 0


def is_whitelisted(username: str | None) -> bool:
    if not username:
        return False
    with _conn() as c:
        row = c.execute(
            "SELECT 1 FROM whitelist WHERE username = ?", (username.lower(),)
        ).fetchone()
        return row is not None


def get_all_whitelist() -> list[dict]:
    with _conn() as c:
        rows = c.execute(
            "SELECT * FROM whitelist ORDER BY added_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]


