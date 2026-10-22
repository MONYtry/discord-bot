
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from api.main import app,set_bot
import asyncio
import uvicorn
from api.tracking import start_tracking

# Läd geheimnisse
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class MyBot(commands.Bot):
    # setup_hook <- Spezial Function von Discord aus
    # Läd alle Module die hier gelisitet sind
    async def setup_hook(self):
        await self.load_extension("cogs.status")
        await self.load_extension("cogs.clear")
        await self.load_extension("cogs.admin")
        await self.load_extension("cogs.join")
        await self.load_extension("cogs.helper")
        await self.load_extension("cogs.embed")
        await self.load_extension("cogs.log")
        await self.load_extension("cogs.support")
        await self.load_extension("cogs.apply")
        await self.load_extension("cogs.moderation")
        await self.load_extension("cogs.reactionroles")
        await self.load_extension("cogs.automoderation")

        # Geht durch jeden Server auf dem der Bot ist
        for guild in self.guilds:
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            print(f"✅ {len(synced)} Commands für {guild.name} synchronisiert")


bot = MyBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():

    placeholder = "―" * 2
    print(
        f"{placeholder}\n"
        f"Bot went online: {bot.user} \n"
        f"{placeholder}\n")

# Falls Token nicht gefunden wird
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN fehlt in der .env-Datei!")

async def start_service():

    # Bot wird in die API übergeben
    set_bot(bot)
    start_tracking(bot)
    # Konfiguriert Server 
    
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8000
    )

    # Server wird an uvicorn übergeben
    server = uvicorn.Server(config)

    # Discord-Bot und Server gleichzeitig Starten
    await asyncio.gather(
        bot.start(TOKEN),
        server.serve()
    )
# Damit nicht der gesamte Bot instant gestartet wird
if __name__ == "__main__":
    asyncio.run(start_service())