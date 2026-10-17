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
            WELCOME_CHANNEL_ID INTEGER)
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

    
def get_bot_status_channel_id(guild_id):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("""
            SELECT BOT_STATUS_CHANNEL_ID
            FROM server_settings
            WHERE guild_id = ?
        """, (str(guild_id),)).fetchone()[0]

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

def set_welcome_channel(guild_id, WELCOME_CHANNEL_ID):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO server_settings(
            guild_id,
            WELCOME_CHANNEL_ID)
            VALUES (?,?)
            ON CONFLICT(guild_id)
            DO UPDATE SET
                WELCOME_CHANNEL_ID = excluded.WELCOME_CHANNEL_ID
        """, (str(guild_id), int(WELCOME_CHANNEL_ID) if WELCOME_CHANNEL_ID else None))

def get_welcome_channel(guild_id):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("""
            SELECT WELCOME_CHANNEL_ID
            FROM server_settings
            WHERE guild_id = ?
        """, (str(guild_id),)).fetchone()[0]
    
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

def get_apply_channel_id(guild_id):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("""
            SELECT apply_channel_id
            FROM server_settings
            WHERE guild_id = ?
        """, (str(guild_id),)).fetchone()[0]


def get_ticket_setting(guild_id):
    with sqlite3.connect(DB_PATH) as con:
        return con.execute("""
            SELECT tickets_enabled 
            FROM server_settings 
            WHERE guild_id = ?
            """, (str(guild_id),)).fetchone()[0]

    return bool(row[0]) if row else False     
load_dataBase()