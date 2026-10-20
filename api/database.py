import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tickets.db")

def load_dataBase():
    with sqlite3.connect(DB_PATH) as conn:
        # Erstellt eine Tabelle
        # Spalten = {id,total_tickets}
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY, 
            total_tickets INTEGER, 
            open_tickets INTEGER,
            closed_tickets INTEGER)
        """)

        # Setzt Werte, falls diese bereits geladen sind <- Skip
        conn.execute("""
            INSERT OR IGNORE INTO stats (
            id,
            total_tickets,
            open_tickets, 
            closed_tickets)

            VALUES(1,0,0,0)
        """)

        # Erstellt eine Tabelle falls sie noch nicht Exisiert
        # Hauptteil = channel_id
        # status = standard 1
        # guild_id = integer
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
            channel_id INTEGER PRIMARY KEY,
            status INTEGER NOT NULL DEFAULT 1,
            guild_id INTEGER)
        """)

        # Erstellt Tabelle für Server_Settings
        # guild_id als String 
        # tickets_enabled als Integer standard 0 = false
        conn.execute("""
            CREATE TABLE IF NOT EXISTS server_settings (
            guild_id TEXT PRIMARY KEY,
            tickets_enabled INTEGER NOT NULL DEFAULT 0,
            apply_channel_id INTEGER,
            BOT_STATUS_CHANNEL_ID INTEGER,
            WELCOME_CHANNEL_ID INTEGER,
            JOIN_LEAVE_LOG_CHANNEL_ID INTEGER,
            BAN_CHANNEL_ID INTEGER,
            SUPPORT_CHANNEL_ID INTEGER, 
            TIMEOUT_LOG_CHANNEL INTEGER,
            MESSAGE_LOG_CHANNEL INTEGER,
            SUPPORT_CHANNEL_LOG_ID INTEGER)
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS supporting_roles (
            guild_id TEXT NOT NULL,
            role_id INTEGER NOT NULL,
            PRIMARY KEY (guild_id, role_id))
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS embed_allowed_roles (
            guild_id TEXT NOT NULL,
            role_id INTEGER NOT NULL,
            PRIMARY KEY (guild_id, role_id))
        """)


def open_ticket(channel_id, status, guild_id):
    with sqlite3.connect(DB_PATH) as conn:
        # SET setzt werte (die rechnung ist selbst erklärend)
        # WHERE id = 1 <- Nutzt ID = 1 (Erkennung)
        conn.execute("""
            UPDATE stats
            SET total_tickets = total_tickets + 1, open_tickets = open_tickets + 1
            WHERE id = 1
        """)

        # INSERT INTO = legt in die Tabelle Werte mit Parameter
        # Fragezeichen sind Placeholder welche durch Parameter erstetzt werden 
        # (Reihenfolge ist entscheident)
        conn.execute("""
            INSERT INTO tickets(channel_id,status,guild_id)
            VALUES(?,?,?)
        """, (channel_id,status,guild_id))

def close_ticket(channel_id,status):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        UPDATE stats
        SET open_tickets = open_tickets - 1, closed_tickets = closed_tickets + 1
        WHERE id = 1
        """)
        
        conn.execute("""
            UPDATE tickets
            SET status = ?
            WHERE channel_id = ?
        """, (channel_id,status))

def get_open_tickets():
    with sqlite3.connect(DB_PATH) as conn:
        # SELECT = Variable / Wert
        # FROM = Tabelle
        return conn.execute("""
            SELECT open_tickets
            FROM stats
        """).fetchone()[0]

def get_closed_tickets():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("""
            SELECT closed_tickets
            FROM stats
        """).fetchone()[0]
    
#.fetchone()[index] = Holt Wert aus der Zeile (index)
def get_total_tickets():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("""
        SELECT total_tickets
        FROM stats
        """).fetchone()[0]
    
def set_support_roles(guild_id: int, role_ids: list[int]):
    role_ids = list(dict.fromkeys(role_ids))
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        DELETE FROM supporting_roles
        WHERE guild_id = ?
        """, (str(guild_id),))
        
        conn.executemany("""
            INSERT INTO supporting_roles (guild_id, role_id)
            VALUES (?,?)
        """, [
            (str(guild_id), int(role_id))
            for role_id in role_ids
        ])
        
def get_support_roles(guild_id: int) -> list[int]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT role_id
            FROM supporting_roles
            WHERE guild_id = ?
        """, (str(guild_id), )).fetchall()
        return [row[0] for row in rows]

def set_embed_allowed_roles(guild_id: int, role_ids: list[int]):
    # Doppelte Rollen-IDs entfernen
    role_ids = list(dict.fromkeys(role_ids))

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            DELETE FROM embed_allowed_roles
            WHERE guild_id = ?
        """, (str(guild_id),))

        conn.executemany("""
            INSERT INTO embed_allowed_roles (guild_id, role_id)
            VALUES (?, ?)
        """, [
            (str(guild_id), int(role_id))
            for role_id in role_ids
        ])

        
def get_embed_allowed_roles(guild_id: int) -> list[int]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT role_id
            FROM embed_allowed_roles
            WHERE guild_id = ?
        """, (str(guild_id),)).fetchall()
        return [row[0] for row in rows]

ALLOWED_COLUMNS = {
    "apply_channel_id",
    "BOT_STATUS_CHANNEL_ID",
    "WELCOME_CHANNEL_ID",
    "JOIN_LEAVE_LOG_CHANNEL_ID",
    "BAN_CHANNEL_ID",
    "SUPPORT_CHANNEL_ID",
    "TIMEOUT_LOG_CHANNEL",
    "MESSAGE_LOG_CHANNEL",
    "SUPPORT_CHANNEL_LOG_ID",
}

def check_column(column_name):
    if column_name not in ALLOWED_COLUMNS:
        raise ValueError(f"Ungültige Spalte: {column_name}")

def set_value_channel(guild_id, column_name, value):
    check_column(column_name)
    # Leere Eingabe -> NULL, sonst als Zahl speichern
    if value:
        value = int(value)
    else:
        value = None

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(f"""
            INSERT INTO server_settings (
            guild_id, 
            {column_name})

            VALUES (?, ?)
            ON CONFLICT(guild_id)
            DO UPDATE SET 
                {column_name} = excluded.{column_name}
        """, (str(guild_id), value))

def get_value_channel(guild_id, column_name):
    check_column(column_name)

    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(f"""
            SELECT {column_name}
            FROM server_settings
            WHERE guild_id = ?
        """, (str(guild_id),)).fetchone()
        return row[0] if row else None
    
def get_bot_status_channel_id(guild_id):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("""
            SELECT BOT_STATUS_CHANNEL_ID
            FROM server_settings
            WHERE guild_id = ?
        """, (str(guild_id),)).fetchone()
        return row[0] if row is not None else None

def set_bot_status_channel_id(guild_id, bot_status_channel_id):
    with sqlite3.connect(DB_PATH) as conn:
        # ON CONFLICT = Falls bereits exisitert => Bearbeiten und ansonsten erstellen
        # DO UPDATE SET = Definiert was geändert werden soll
        # excluded. = Wert der gesetz werden soll
        # Falls kein Status Channel gesetzt wurde Null in der Datenbank speichernm
        conn.execute("""
            INSERT INTO server_settings (
                guild_id,
                BOT_STATUS_CHANNEL_ID
            )
            VALUES (?, ?)
            ON CONFLICT(guild_id)
            DO UPDATE SET
                BOT_STATUS_CHANNEL_ID = excluded.BOT_STATUS_CHANNEL_ID
        """, (str(guild_id), int(bot_status_channel_id) if bot_status_channel_id else None))

def get_welcome_channel(guild_id):
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("""
            SELECT welcome_channel_id
            FROM server_settings
            WHERE guild_id = ?
        """, (str(guild_id),)).fetchone()

        if result is None:
            return None
        return result[0]

def get_support_channel_log(guild_id):
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("""
            SELECT SUPPORT_CHANNEL_LOG_ID
            FROM server_settings
            WHERE guild_id = ?
        """, (str(guild_id),)).fetchone()
    
        if result is None:
            return None
        return result[0]
    

def get_message_log_channel(guild_id):
     with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("""
            SELECT MESSAGE_LOG_CHANNEL
            FROM server_settings
            WHERE guild_id = ?
        """, (str(guild_id),)).fetchone()
        if result is None:
            return None
        return result[0]

def get_timeout_channel(guild_id):
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("""
            SELECT TIMEOUT_LOG_CHANNEL
            FROM server_settings
            WHERE guild_id = ?
        """, (str(guild_id), )).fetchall()
        if result is None:
            return None
        return result[0]

def save_ticket_setting(guild_id, enabled, apply_channel_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO server_settings (
                guild_id,
                tickets_enabled,
                apply_channel_id
            )
            VALUES (?, ?, ?)
            ON CONFLICT(guild_id)
            DO UPDATE SET
                tickets_enabled = excluded.tickets_enabled,
                apply_channel_id = excluded.apply_channel_id
        """, (str(guild_id), int(enabled), int(apply_channel_id) if apply_channel_id else None))

def get_ticket_setting(guild_id):
    with sqlite3.connect(DB_PATH) as con:
        return con.execute("""
            SELECT tickets_enabled 
            FROM server_settings 
            WHERE guild_id = ?
            """, (str(guild_id),)).fetchone()[0]
    return bool(row[0]) if row else False

def get_leave_join_log_channel(guild_id):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("""
            SELECT JOIN_LEAVE_LOG_CHANNEL_ID
            FROM server_settings
            WHERE guild_id = ?
        """, (str(guild_id),)).fetchone()
        return row[0] if row is not None else None

def get_ban_log_channel(guild_id):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("""
            SELECT BAN_CHANNEL_ID
            FROM server_settings
            WHERE guild_id = ?
        """, (str(guild_id),)).fetchone()
        return row[0] if row is not None else None

def get_apply_channel_id(guild_id):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("""
            SELECT apply_channel_id
            FROM server_settings
            WHERE guild_id = ?
        """, (str(guild_id),)).fetchone()
        return row[0] if row is not None else None

def get_support_channel_id(guild_id):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("""
            SELECT SUPPORT_CHANNEL_ID
            FROM server_settings
            WHERE guild_id = ?
        """, (str(guild_id),)).fetchone()
        return row[0] if row is not None else None

load_dataBase()