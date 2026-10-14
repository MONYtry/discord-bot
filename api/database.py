import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tickets.db")
DB_PATH = os.path.abspath(DB_PATH)


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                channel_id INTEGER PRIMARY KEY,
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                closed_at TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY CHECK (id = 99),
                total_tickets INTEGER DEFAULT 0,
                total_closed_tickets INTEGER DEFAULT 0
            )
        """)

        # Fehlende Spalte in der alten Datenbank ergänzen
        columns = [
            row[1]
            for row in conn.execute("PRAGMA table_info(stats)")
        ]

        if "total_closed_tickets" not in columns:
            conn.execute("""
                ALTER TABLE stats
                ADD COLUMN total_closed_tickets INTEGER DEFAULT 0
            """)

        conn.execute("""
            INSERT OR IGNORE INTO stats
                (id, total_tickets, total_closed_tickets)
            VALUES (99, 0, 0)
        """)


def create_ticket(channel_id, guild_id, user_id, category):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO tickets
                (channel_id, guild_id, user_id, category)
            VALUES (?, ?, ?, ?)
        """, (channel_id, guild_id, user_id, category))

        conn.execute("""
            UPDATE stats
            SET total_tickets = total_tickets + 1
            WHERE id = 99
        """)


def close_ticket(channel_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("""
            UPDATE tickets
            SET closed_at = CURRENT_TIMESTAMP
            WHERE channel_id = ? AND closed_at IS NULL
        """, (channel_id,))

        if cursor.rowcount > 0:
            conn.execute("""
                UPDATE stats
                SET total_closed_tickets = total_closed_tickets + 1
                WHERE id = 99
            """)


def get_total_closed_tickets():
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("""
            SELECT total_closed_tickets
            FROM stats
            WHERE id = 99
        """).fetchone()

        return result[0] if result else 0


def get_total_tickets():
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("""
            SELECT total_tickets
            FROM stats
            WHERE id = 99
        """).fetchone()

        return result[0] if result else 0


def get_open_tickets():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("""
            SELECT COUNT(*)
            FROM tickets
            WHERE closed_at IS NULL
        """).fetchone()[0]


init_db()
