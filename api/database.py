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

load_dataBase()