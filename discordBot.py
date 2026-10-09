import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import os


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!",intents=intents)

TOKEN = os.getenv("DISCORD_TOKEN")
channel_id = 1558243145836269568
GUILD_ID = 1557487186016993363  

@bot.event
async def on_ready():
    
    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    synced = await bot.tree.sync(guild=guild)

    print(f"Bot erfolgreich Command-Syncronisiert {[cmd.name for cmd in synced]}")

    print(f"Discord-Bot ist erfolgreich Online {bot.user}")
    channel = bot.get_channel(channel_id)
    
    if channel is not None:
        await channel.send(f"Bot-Status: Läuft :hearts:")
        #await deleteMessages(channel_id,2)

    else:
        print("Channel nicht gefunden")

@bot.tree.command(name="shutdown", description="Nimmt den Bot offline")
async def shutdown(interaction: discord.Interaction):
    print("Shutdown-Command wurde aufgerufen!")
    if not await bot.is_owner(interaction.user):
        await interaction.response.send_message("Du hast dazu keine Rechte!", ephemeral=True)
        return

    await interaction.response.send_message("🔴 Bot geht offline", ephemeral=True)

    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send("🔴 Bot geht offline")

    await asyncio.sleep(2)
    await bot.close()

def startBot():
    # Startet den Discord-Bot mit angegeben Token
    bot.run(TOKEN)


# Erstellt Tab zum Auswählen (Command)
@bot.tree.command(name="clear", description="Deletes an amount of messages in the current Channel")
# Erstellt Platzhalter zum Angeben der Anzahl
@discord.app_commands.describe(amount="Amount of messages to delete!")
async def deleteMessages(
    # Nutzt Interaction
    interaction: discord.Interaction,
    # Holt sich die Anzahl von dem aktuellen Command
    # Von 1 bis 100 maximale Anzahl
    amount: discord.app_commands.Range[int,1,100]):

    # Signalisiert das ein Command verarbeitet wird, antwort bleibt privat
    await interaction.response.defer(ephemeral=True)

    # Löscht Nachrichten im Channel wo der Befehl ausgeführt wurde
    # Löscht Nachrichten nur maximal bis amount anzahl
    deleted = await interaction.channel.purge(limit=amount)

    # Sobald der Command ausgeführt wurde eine Nachricht Anzeigen!
    await interaction.followup.send(f"🗑️ {len(deleted)} Nachrichten erfolgreich gelöscht!", ephemeral=True)

startBot()
