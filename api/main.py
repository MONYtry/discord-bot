from fastapi import FastAPI
import asyncio
import time
from fastapi.middleware.cors import CORSMiddleware
from api.database import get_total_tickets,get_open_tickets,get_closed_tickets
import httpx
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import os
import secrets
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
    # Nur lokal
    https_only=False,  
)

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://127.0.0.1:5500"],
                   allow_methods=["GET"],
                   allow_headers=["*"],
                   allow_credentials=True)

bot = None
start_time = None
oauth_tokens = {}



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
async def auth_login(request: Request):
    if await auth_status(request):
        return RedirectResponse("http://127.0.0.1:5500/website/landingPage/ladingPage.html",status_code=303)
        

    # Erstellt einen 32-Stelligen String 
    state = secrets.token_urlsafe(32)
    request.session["oauth_state"] = state
    
    # Erstellt benötigte Parameter
    parameter = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "identify guilds",
        "state": state,
    }

    from urllib.parse import urlencode
    # Erstellt finale URL
    discord_url = ("https://discord.com/oauth2/authorize?" + urlencode(parameter))
    return RedirectResponse(discord_url)

@app.get("/auth/callback")
async def auth_callback(request: Request, code: str | None = None, state: str | None = None):
    # Prüft ob Discord den erwarteten Sicherheitswert zurückgibt
    except_state = request.session.pop("oauth_state", None)

    # Falls etwas schief läuft
    if not code or not state or state != except_state:
        return HTMLResponse("Login Fehlgeschlagen: Ungülitiger state.", status_code=400)
    
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://discord.com/api/oauth2/token", 
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI
            },
        )

        # Falls Discord nicht richtig Antwortet
        if token_response.status_code != 200:
            return HTMLResponse("Discord-Token konnte nicht abgerufen werden.",status_code=400,)
        
        # Macht aus token_response eine normae Variable
        token_data = token_response.json()
        # Holt sich accsess token
        accesses_token = token_data["access_token"]
        
        # Baut Server Response
        guild_response = await client.get(
            "https://discord.com/api/users/@me/guilds",
            headers= {
                "Authorization": f"Bearer {accesses_token}"
            },
        )
        
        # Falls blockiert wurde
        if guild_response.status_code != 200:
            return HTMLResponse("Discord-Server konnten nicht geladen werden.", status_code=400,)
        guilds = guild_response.json()
        
        # Baut User Response
        user_response = await client.get(
            "https://discord.com/api/users/@me",
            headers={
                "Authorization": f"Bearer {accesses_token}"
            },
        )
        # Falls blockiert wird
        if user_response.status_code != 200:
            return HTMLResponse("Discord-Token konnte nicht abgerufen werden.",status_code=400,)
        
        user = user_response.json()


        aviliable_guilds = []
        # Geht durch alle Server, auf welchem der Bot ist
        for user_guild in guilds:
            # Geht durch alle Server auf den der Bot ist
            for bot_guild in bot.guilds:
                # Falls Server übereinstimmen
                if user_guild["id"] == str(bot_guild.id):
                    if user_guild["owner"]:
                        print("Inhaber des Servers")
                    else:
                        print("Nur Mitglied des Servers")

                    # Fügt den Server in den Array
                    aviliable_guilds.append(user_guild)


        # Gibt alles zurück
        session_id = secrets.token_urlsafe(32)

        oauth_tokens[session_id] = accesses_token
        request.session["session_id"] = session_id

        return RedirectResponse("http://127.0.0.1:5500/website/landingPage/ladingPage.html",status_code=303)
        return {
        "message": "Discord-Login erfolgreich!",
        "user_id": user["id"],
        "username": user["username"],
        "guilds": [
            {
                "id": guild["id"],
                "name": guild["name"],
                "icon": guild["icon"],
                "permissions": guild["permissions"],
            }
            for guild in aviliable_guilds
        ]
    }
@app.get("/auth/status")
async def auth_status(requests: Request):
    # Holt sich die gespeicherte Session ID
    session_id = requests.session.get("session_id")
    # Holt sich den gespeicherten Token
    token = oauth_tokens.get(session_id)
    
    # Falls kein Token gefunden wurde
    if not token:
        return False
    return True
    
@app.get("/api/guilds")
async def get_user_guilds(requests: Request):
    # Holt sich die gespeicherte Session ID
    session_id = requests.session.get("session_id")
    # Holt sich den gespeicherten Token
    token = oauth_tokens.get(session_id)

    # Falls kein Token gefunden wurde
    if not token:
        return HTMLResponse("Bitte zuerst anmelden.", status_code=401)


    async with httpx.AsyncClient() as client:
        response = await client.get( "https://discord.com/api/users/@me/guilds",
            headers={"Authorization": f"Bearer {token}"}
        )

        if response.status_code == 429:
           data = response.json()
           await asyncio.sleep(data.get("retry_after",1))

           response = await client.get("https://discord.com/api/users/@me/guilds",headers={"Authorization": f"Bearer {token}"})

        user_guilds = response.json()
        aviliable_guilds = []

        # Geht durch alle Server, auf welchem der Bot ist
        for user_guild in user_guilds:
            # Geht durch alle Server auf den der Bot ist
            for bot_guild in bot.guilds:
                # Falls Server übereinstimmen
                if user_guild["id"] == str(bot_guild.id):
                    # Fügt den Server in den Array
                    aviliable_guilds.append(user_guild)

        return aviliable_guilds
