from fastapi import FastAPI
import time
from fastapi.middleware.cors import CORSMiddleware
from api.database import get_open_tickets,get_total_tickets,get_total_closed_tickets

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=["http://127.0.0.1:5500"],
                   allow_methods=["GET"],
                   allow_headers=["*"])

bot = None
start_time = None

def set_bot(discord_bot):
    global bot,start_time
    bot = discord_bot
    start_time = time.time()

# STARTING COMMAND:
# python -m uvicorn api.main:app --reload
# unvicorn = Startet Webserver
# api.main = Sucht in dem Ordner (API) eine Datei (main)
# :app verwendet die Variable app
# --reload = Startet die API neu bei Code änderungen

# Registriert eine Route für HTTP-GET Anfragen an /
# "/" = standard request (home)
@app.get("/")
def home(): # home() wird aufgerufen sobald API gecalled wird
    return{"message": "API läuft!"}


def getTime():
    # Rechnet von der aktuellen Zeit - start_time
    uptime_seconds = int(time.time() - start_time)
    
    # Durch // wird keine Kommazahl gemacht
    days = uptime_seconds // 86400
    # Gibt den Wert der Division zurück und nutzt diesen
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60

    uptime = f"{days}d {hours}h {minutes}m {seconds}s"
    return uptime

def getBotOnline():
    if bot is None or bot.is_ready() is False:
        return False
    return True

def getMembersCount():
    # Setzt Member_Count auf 0
    member_count = 0
    # Geht durch alle Server
    for server in bot.guilds:
        # Holt sich die Mitglieder-Anzahl
        # Falls Fehler Auftritt setzt es 0
        member_count += server.member_count or 0
    return member_count

@app.get("/status")
def status():
    if getBotOnline() is False:
        return {
            "bot_online": False,
            "message": "Bot hasn't loaded"
        }
        
    raw_ping = bot.latency
    ping = round(raw_ping * 1000)

    return {
            "bot_online": True,
            "username": str(bot.user),
            "ping_ms": ping,
            "uptime": getTime(),
            "api_status": "online",
            "message": "Bot ist online"
        }


@app.get("/stats")
def stats():
    if getBotOnline() is False:
        return {
            "message": "Bot hasn't loaded"
        }

    return {
        "guild_count": len(bot.guilds),
        "user_count": getMembersCount(),
        "cog_count": len(bot.extensions),
        "open_tickets": get_open_tickets(),
        "total_tickets": get_total_tickets(),
        "total_closed_tickets": get_total_closed_tickets()
    }

@app.get("/guilds")
def guilds():
    if getBotOnline() is False:
        return {
            "message": "Bot hasn't loaded"
        }

    guild_list = []
    for server in bot.guilds:
        guild_list.append({
            "id": str(server.id),
            "name": server.name,
            "member_count": server.member_count
        })

    return {
        "guild_count":  len(guild_list),
        "guilds": guild_list
    }


@app.get("/commands")
def commands():
    command_list = []
    for command in bot.tree.get_commands():
        command_list.append({
            "name": command.name,
            "description": command.description
        })
        
    return {
        "command_count": len(command_list),
        "commands": command_list
    }