from discord.ext import tasks
from api.database import save_member_count

bot = None

@tasks.loop(minutes=1)
async def daily_member_tracking():
    if bot is None:
        return

    for guild in bot.guilds:
        try:
            member_count = guild.member_count

            if member_count is None:
                print(f"⚠️ Mitgliederzahl für {guild.name} nicht verfügbar.")
                continue

            save_member_count(guild.id, member_count)

            print(f"📊 {guild.name}: {member_count} Mitglieder gespeichert.")

        except Exception as error:
            print(f"❌ Fehler beim Tracking für {guild.name}: {error}")

@daily_member_tracking.before_loop
async def before_tracking():
    await bot.wait_until_ready()


def start_tracking(discord_bot):
    global bot
    bot = discord_bot

    if not daily_member_tracking.is_running():
        daily_member_tracking.start()