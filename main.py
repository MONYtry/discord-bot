
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from config import SERVER_ID

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
        await self.load_extension("cogs.moderation")
        await self.load_extension("cogs.reactionroles")
        await self.load_extension("cogs.automoderation")

        # Slash-Commands registierieren
        guild = discord.Object(id=SERVER_ID)

        # Cleared die alten Commands
        #self.tree.clear_commands(guild=None)
        
        self.tree.copy_global_to(guild=guild)
        synced = await self.tree.sync(guild=guild)
        print(f"✅ {len(synced)} Slash-Commands synchronisiert!")

bot = MyBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot ist online: {bot.user}")

# Falls Token nicht gefunden wird
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN fehlt in der .env-Datei!")

bot.run(TOKEN)
