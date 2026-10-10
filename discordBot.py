import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import os
import datetime


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!",intents=intents)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

isBotOnline = False

BOT_STATUS_CHANNEL_ID = 1558243145836269568
GUILD_ID = 1557487186016993363  

@bot.event
async def on_ready():
    global isBotOnline
    isBotOnline = True

    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    synced = await bot.tree.sync(guild=guild)

    print(f"Bot erfolgreich Command-Syncronisiert {[cmd.name for cmd in synced]}")

    print(f"Discord-Bot ist erfolgreich Online {bot.user}")
    
    channel = bot.get_channel(BOT_STATUS_CHANNEL_ID)

    if channel is not None:
        deleted = await channel.purge(limit=10)
        print(f"🗑️  {len(deleted)} alte Nachrichten gelöscht!")
        if await send_status_embed(BOT_STATUS_CHANNEL_ID) is False:
            await channel.send(f"Bot-Status: Läuft :green_circle:")

    else:
        print("Channel nicht gefunden")

@bot.tree.command(name="shutdown", description="Nimmt den Bot offline")
async def shutdown(interaction: discord.Interaction):
    global isBotOnline
    
    print("Shutdown-Command wurde aufgerufen!")
    
    if not await bot.is_owner(interaction.user):
        await interaction.response.send_message("Du hast dazu keine Rechte!", ephemeral=True)
        return

    await interaction.response.send_message("🔴 Bot geht offline", ephemeral=True)
    
    channel = bot.get_channel(BOT_STATUS_CHANNEL_ID)
    isBotOnline = False

    if channel:
        deleted = await interaction.channel.purge(limit=3)
        if await send_status_embed(BOT_STATUS_CHANNEL_ID) is False:
            await channel.send("🔴 Bot-Status: Offline ")

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



async def send_status_embed(channelID):

    date = datetime.datetime.now()
    currentTime = date.strftime("%d/%m/%Y • %H:%M")
    status = "🟢 Online" if isBotOnline else "🔴 Offline"
    embed = discord.Embed(
        title=":hotsprings: Bot-Status",
        description=f"Hier wird der aktuelle Status des Discord-Bots angezeigt!",
        color=discord.Color.blue())
    embed.add_field(name="Status", value = status, inline = True)
    embed.add_field(name="Version", value = "1.0 Beta", inline = True)
    embed.add_field(name="Letzte Aktualisierung", value = currentTime, inline = True)

    

    embed.set_footer(text=f"Developer Academy Bot • Made with Love ❤️")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1534607507023069346/1558267347754819604/ChatGPT_Image_7._Okt._2026_22_52_37.png?ex=6acad10e&is=6ac97f8e&hm=db7aea039edc7e4d1a7a99e68c54a1e4fc5510a4d2fa58c0472a73ebf5322c1c&")
    
    channelToUse = bot.get_channel(channelID)
    if channelToUse is not None:
        await channelToUse.send(embed=embed)
        return True
    return False
startBot()
