
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Läd geheimnisse
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    # setup_hook <- Spezial Function von Discord aus
    # Läd alle Module die hier gelisitet sind
    async def setup_hook(self):
        await self.load_extension("cogs.status")
        await self.load_extension("cogs.clear")
        await self.load_extension("cogs.admin")

        # Slash-Commands für deinen Server synchronisieren
        guild = discord.Object(id=1557487186016993363)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

bot = MyBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot ist online: {bot.user}")
    

# Falls Token nicht gefunden wird
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN fehlt in der .env-Datei!")

bot.run(TOKEN)
