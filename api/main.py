from fastapi import FastAPI
import asyncio
import time
from fastapi.middleware.cors import CORSMiddleware
from api.database import DB_PATH

from api.database import (
    get_total_tickets,
    get_open_tickets,
    get_closed_tickets,
    save_ticket_setting,
    get_ticket_setting,
    set_welcome_channel,
    set_ban_log_channel,
    set_leave_join_log_channel,
    set_bot_status_channel_id,
    get_bot_status_channel_id,
    get_apply_channel_id,
    get_leave_join_log_channel,
    get_welcome_channel,
    get_ban_log_channel,
    get_support_channel_id,
    set_support_channel_id,
    get_timeout_channel,
    set_timeout_channel,
    get_message_log_channel,
    set_message_log_channel,
    get_support_channel_log,
    set_support_channel_log,
    get_embed_allowed_roles,
    set_embed_allowed_roles
)
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")
SESSION_SECRET = os.getenv("SESSION_SECRET")

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    same_site="lax",
    max_age=3600,
    # Nur lokal
    https_only=False
)

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://127.0.0.1:5500"],
                   allow_methods=["GET", "POST"],
                   allow_headers=["*"],
                   allow_credentials=True)

bot = None
start_time = None
oauth_tokens = {}

saved_tokens = []


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
        "total_closed_tickets": get_closed_tickets()
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
    if bot is None:
        print("Error")
        return
    
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

@app.get("/auth/login")
async def auth_logging():
    # Werte über die Anfrage
    # client_id = Anwendungs ID
    # redirect_uri = Wohin zurück geben
    # response_type = Autorisierungscode
    # scope = Was wir erhalten wollen (profil)
    parameter = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "identify guilds",
    }
    from urllib.parse import urlencode

    discord_url = "https://discord.com/oauth2/authorize?" + urlencode(parameter)
    return RedirectResponse(discord_url)


@app.get("/auth/callback")
async def auth_callback(request: Request, code: str | None = None, error: str | None = None):
    if error:
        print("Fehler", error)

    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://discord.com/api/oauth2/token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI
            }
        )

        if token_response.status_code != 200:
            print("Etwas ist schief gelaufen (token_Response)")
        # Macht aus Json -> Dicanary
        token_data = token_response.json()

        # Holt sich den Accsess Token aus der Antwort
        accsess_token = token_data["access_token"]
        saved_tokens.append(accsess_token)

        user_response = await client.get(
            "https://discord.com/api/v10/users/@me",
            headers= {"Authorization": f"Bearer {accsess_token}"}
        )

        if user_response.status_code != 200:
             print("Etwas ist schief gelaufen (user_response)")
        
        user_data = user_response.json()
        # Erstellt eine Session
        # Name der Session wird in den Klammern Definiert
        # Alles was innerhalb der geschweiften Klammern steht ist verfügbarer Inhalt
        request.session["discord_user"] = {
            "id": user_data["id"],
            "username": user_data["username"],
            "avatar": user_data.get("avatar"),
            "saved_token": accsess_token
        }
        # Schickt Nutzer zurück auf die Startseite 
        return RedirectResponse(url="http://127.0.0.1:5500/website/landingPage/ladingPage.html")


@app.get("/auth/me")
async def get_current_user(request: Request):
    # Holt sich anhand der Anfrage die Session
    user = request.session.get("discord_user")
    # Falls keine Session gefunden wurde
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Nicht angemeldet"
        )

    # Gibt die Nutzer-Daten zurück
    return user



@app.get("/auth/guilds")
async def getUserGuilds(request: Request):
    # Holt sich den User
    user = request.session.get("discord_user")
    # Falls er keinen User findet 
    if not user:
        raise HTTPException(status_code=401, detail="Nicht angemeldet")
    # Holt sich den savedToken aus der Session
    access_token = user.get("saved_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Access Token fehlt")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://discord.com/api/v10/users/@me/guilds",
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )

        if response.status_code != 200:
                raise HTTPException(status_code=502, detail=f"Discord API Fehler: {response.status_code}")
        
    all_guilds = []
    user_guilds = response.json()

    # Geht durch alle Server wo der Bot ist
    for guild in user_guilds:
        guild_id = int(guild["id"])
        if bot.get_guild(guild_id) is not None:
            if guild["owner"]:
                all_guilds.append(guild)

    
    return all_guilds


@app.post("/auth/logout")
async def get_current_user(request: Request):
    # Löscht alles aus der Session
    request.session.clear()
    return {"message": "Erfolgreich ausgeloggt"}

@app.post("/servers/{guild_id}/settings")
async def save_settings(guild_id: str, request: Request):
    user = request.session.get("discord_user")

    if not user:
        raise HTTPException(status_code=401)

    # Owner-Prüfung wie im GET-Endpoint
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://discord.com/api/v10/users/@me/guilds",
            headers={
                "Authorization": f"Bearer {user['saved_token']}"
            }
        )

    if response.status_code != 200:
        raise HTTPException(status_code=502)

    is_owner = False

    for guild in response.json():
        if guild["id"] == guild_id and guild["owner"]:
            is_owner = True
            break

    if not is_owner:
        raise HTTPException(status_code=403)

    data = await request.json()

    tickets_enabled = data.get("tickets_enabled") is True
    apply_channel_id = data.get("Input_Apply_Channel_ID")
    bot_status_channel_id = data.get("Input_Status_Channel_ID")
    welcome_channel_id = data.get("Input_Welcome_Channel_ID")
    ban_channel_id = data.get("Input_Ban_Channel_ID")
    join_leave_log_channel_id = data.get("Input_Join_Leave_Log_Channel_ID")
    support_channel_id = data.get("support_channel_id")
    timeout_channel_id = data.get("timeout_channel_id")
    message_channel_id = data.get("message_channel_id")
    support_log_channel_id = data.get("support_log_channel_id")
    embed_allowed_roles = data.get("embed_allowed_roles")

    # Save Ticket Setting
    save_ticket_setting(guild_id, tickets_enabled, apply_channel_id)
    
    # NORMAL CHANNELS
    set_bot_status_channel_id(guild_id, bot_status_channel_id)
    set_welcome_channel(guild_id,welcome_channel_id)
    set_embed_allowed_roles(guild_id,embed_allowed_roles)
    # LOG CHANNEL
    set_support_channel_log(guild_id,support_log_channel_id)
    set_message_log_channel(guild_id,message_channel_id)
    set_ban_log_channel(guild_id,ban_channel_id)
    set_leave_join_log_channel(guild_id,join_leave_log_channel_id)
    set_support_channel_id(guild_id,support_channel_id)
    set_timeout_channel(guild_id, timeout_channel_id)

    return {
        "tickets_enabled": tickets_enabled,
        "apply_channel_id": apply_channel_id,
        "statusInput": bot_status_channel_id,
        "welcomeChannelInput": welcome_channel_id,
        "join_leave_log_channel_id": join_leave_log_channel_id,
        "ban_channel_id": ban_channel_id,
        "support_channel_id": support_channel_id,
        "timeout_channel_id": timeout_channel_id,
        "message_channel_id": message_channel_id,
        "support_log_channel_id": support_log_channel_id,
        "embed_allowed_roles": embed_allowed_roles
    }




def save_setting(guild_id, setting, value):
    allowed = {
        "tickets_enabled",
        "apply_channel_id",
        "BOT_STATUS_CHANNEL_ID",
        "welcome_channel_id"
    }

    if setting not in allowed:
        raise ValueError("Ungültige Einstellung")
    
    if setting == "tickets_enabled":
        value = int(value)

    with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
            f"""
            INSERT INTO server_settings (guild_id, {setting})
            VALUES (?, ?)
            ON CONFLICT(guild_id)
            DO UPDATE SET {setting} = excluded.{setting}
            """,
            (str(guild_id), value)
        )


@app.get("/servers/{guild_id}/settings")
async def getSettings(guild_id: str, request: Request):
    if not request.session.get("discord_user"):
        raise HTTPException(status_code=401, detail="Nicht eingeloggt")
    
    status_channel_id = get_bot_status_channel_id(guild_id)
    welcome_channel_id = get_welcome_channel(guild_id)
    join_leave_channel_id = get_leave_join_log_channel(guild_id)
    ban_log_channel_id = get_ban_log_channel(guild_id)
    apply_channel_id = get_apply_channel_id(guild_id)
    ticket_setting = get_ticket_setting(guild_id)
    support_channel_id = get_support_channel_id(guild_id)
    timeout_channel_id = get_timeout_channel(guild_id)
    message_channel_id = get_message_log_channel(guild_id)
    support_channel_id = get_support_channel_log(guild_id)
    embed_allowed_roles = get_embed_allowed_roles(guild_id)

    return {
        "apply_channel_id": apply_channel_id,
        "statusInput": status_channel_id,
        "welcomeChannelInput": welcome_channel_id,
        "join_leave_log_channel_id": join_leave_channel_id,
        "ban_channel_id": ban_log_channel_id,
        "apply_channel_id": apply_channel_id,
        "tickets_enabled": ticket_setting,
        "support_channel_id": support_channel_id,
        "timeout_channel_id": timeout_channel_id,
        "message_channel_id": message_channel_id,
        "support_log_channel_id": support_channel_id,
        "embed_allowed_roles": embed_allowed_roles
    }