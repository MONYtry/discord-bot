import sqlite3
import os

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
BERLIN_TZ = ZoneInfo("Europe/Berlin")


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

        conn.execute("""
            CREATE TABLE IF NOT EXISTS admin_perm_roles (
            guild_id INTEGER NOT NULL,
            role_id INTEGER NOT NULL,
            PRIMARY KEY (guild_id, role_id))
        """)

         # Mitgliederverlauf für Tests im Minutentakt
        conn.execute("""
            CREATE TABLE IF NOT EXISTS member_history_minutes (
                guild_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                member_count INTEGER NOT NULL,
                PRIMARY KEY (guild_id, timestamp)
            )
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
    


ALLOWED_ROLE_TABLES = {
    "supporting_roles",
    "admin_perm_roles",
    "embed_allowed_roles",
}


def set_role_id_list(guild_id: int, role_ids: list[int], dbName: str):
    if dbName not in ALLOWED_ROLE_TABLES:
        raise ValueError(f"Ungültige Rollentabelle: {dbName}")

    role_ids = list(dict.fromkeys(int(role_id) for role_id in role_ids))

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            DELETE FROM supporting_roles
            WHERE 0
        """) if False else None

        conn.execute(
            f"DELETE FROM {dbName} WHERE guild_id = ?",
            (str(guild_id),)
        )

        conn.executemany(
            f"""
            INSERT INTO {dbName} (guild_id, role_id)
            VALUES (?, ?)
            """,
            [(str(guild_id), role_id) for role_id in role_ids]
        )

    
def get_role_id_list(guild_id: int, dbName) -> list[int]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(f"""
            SELECT role_id
            FROM {dbName}
            WHERE guild_id = ?
        """, (str(guild_id), )).fetchall()
        return [row[0] for row in rows]


def set_admin_perm_roles(guild_id: int, role_ids: list[int]):
    role_ids = list(dict.fromkeys(role_ids))

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            DELETE FROM admin_perm_roles
            WHERE guild_id = ?
        """, (str(guild_id),))

        conn.executemany("""
            INSERT INTO admin_perm_roles (guild_id, role_id)
            VALUES (?, ?)
        """, [
            (str(guild_id), int(role_id))
            for role_id in role_ids
        ])

def get_admin_perm_roles(guild_id: int) -> list[int]:
     with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute("""
                SELECT role_id
                FROM admin_perm_roles
                WHERE guild_id = ?
            """, (str(guild_id),)).fetchall()
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
        if row is None or row[0] is None:
            return None
        return int(row[0])
    

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


def save_member_count(guild_id, member_count):
    timestamp = datetime.now(BERLIN_TZ).strftime("%Y-%m-%dT%H:%M")

    print(f"[TRACKING DB] {DB_PATH} | Guild: {guild_id} | Members: {member_count}")

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO member_history_minutes (
            guild_id, 
            timestamp, 
            member_count)

            VALUES (?,?,?)
            ON CONFLICT (guild_id,timestamp)
            DO UPDATE SET 
                member_count = excluded.member_count
        """, (str(guild_id), timestamp, int(member_count)))

def get_member_history(guild_id, minutes=5):
    now = datetime.now(BERLIN_TZ).replace(second=0, microsecond=0)
    fmt = "%Y-%m-%dT%H:%M"
    start_time = now - timedelta(minutes=minutes)

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT timestamp, member_count
            FROM member_history_minutes
            WHERE guild_id = ? AND timestamp <= ?
            ORDER BY timestamp ASC
        """, (str(guild_id), now.strftime(fmt))).fetchall() # Fetchall = holt alle Ergebnisse

    history = []
    for row in rows:
        # Holt sich aus den Zeilen bestimmte Werte, danach werden sie in einen Dictanary gespeichert
        history.append({"date": row[0], "member_count": row[1]})
    
    result = []
    last_count = None

    for i in range(minutes + 2):
        neue_zeit = start_time + timedelta(minutes=i)
        timestamp = neue_zeit.strftime(fmt)
        
        # Geht durch alle Ergebnise 
        for entry in history:
            # Falls in der History ein Eintrag mit "date" exisitert
            # und dieser älter als die aktuelle zeit ist
            if entry["date"] <= timestamp:
                # Erstellt eine Variable welche mit der 
                # Mitglieder-Anzahl des Eintrags bestückt wird
                last_count = entry["member_count"]
            else:
                break
        if last_count is not None:
            result.append({"date": timestamp, "member_count": last_count})

    return result

load_dataBase()