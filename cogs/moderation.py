import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
from config import TIMEOUT_ALLOWED_ROLE_IDS, NO_RIGHTS_MESSAGE,SUPPORT_THUMBNAIL_URL
from api.database import get_timeout_channel
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.already_logged = False

    @commands.Cog.listener()
    async def on_ready(self):
        if self.already_logged:
            return
                
        self.already_logged = True
        helper_cog = self.bot.get_cog("Helper")
        await helper_cog.logMessage("moderation.py","Succcsessfully loaded")
    
    # Platzhalter
    @app_commands.describe(
    user="Der User, der einen Timeout bekommen soll",
    duration="Dauer des Timeouts",
    timetype="Minuten, Stunden oder Tage",
    reason="Grund für den Timeout"
    )

    @app_commands.command(name="timeout", description="Gibt einem User einen Timeout")
    
    # Auswahl der Zeit-Einheiten
    @app_commands.choices(timetype=[
        app_commands.Choice(name="Minuten", value="minuten"),
        app_commands.Choice(name="Stunden", value="stunden"),
        app_commands.Choice(name="Tage", value="tage")
    ])

    async def timeout(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        duration: int,
        timetype: app_commands.Choice[str],
        reason: str = "Kein Grund angegeben"):

        has_permission = any(role.id in TIMEOUT_ALLOWED_ROLE_IDS for role in interaction.user.roles)
        
        # Wenn der Nutzer keine Rechte hat
        if not has_permission:
                    await interaction.response.send_message(NO_RIGHTS_MESSAGE, ephemeral=True)
                    return
        time_units = {
            "minuten": timedelta(minutes=1),
            "stunden": timedelta(hours=1),
            "tage": timedelta(days=1)
        }

        if duration < 1:
            await interaction.response.send_message("❌ Die Dauer muss mindestens 1 sein!", ephemeral=True)
            return
        
        # Zeit wird berechnet
        dauer_zeit = time_units[timetype.value] * duration
        channel_id = get_timeout_channel(interaction.guild_id)
        # Kleiner Bug behoben
        channel_id = channel_id[0]
        if channel_id is None:
             print(f"Es wurde kein Channel zum logen des Timeoutes gefunden")
        print(channel_id)
        channel = self.bot.get_channel(channel_id)
        helper_cog = self.bot.get_cog("Helper")

        try:
            if user.is_timed_out():
                await user.timeout(None, reason="Timeout aufgegeben")
                await interaction.response.send_message(f"Timeout von {user.mention} wurde aufgehoben", ephemeral=True)
                await helper_cog.send_embed(
                                    channel,
                                    "Member Timeout removed",
                                    f"🔨 **User timeout removed!**\n"
                                    f"👤 User: {user.mention} (`{user.id}`)\n", 
                                    discord.Color.green(),user.avatar.url,SUPPORT_THUMBNAIL_URL)
                return
            
            await user.timeout(dauer_zeit, reason=reason)

        except discord.Forbidden as e:
            await interaction.response.send_message(
                f"❌ Keine Berechtigung für den Timeout!\n" 
                f"Details: {e.text}", ephemeral=True
            )
        
        await interaction.response.send_message(f"{user.mention} wurde getimeoutet für {duration} {timetype.name}", ephemeral=True)

        
        if channel:
            if helper_cog:
                await helper_cog.send_embed(
                    channel,
                    "Member was timeoutet",
                    f"🔨 **User timeoutet!**\n"
                    f"👤 User: {user.mention} (`{user.id}`)\n"
                    f"⏳ Dauer: {duration} {timetype.name}\n"
                    f"📝 Grund: {reason}"
                    ,discord.Color.red(), user.avatar.url,SUPPORT_THUMBNAIL_URL
                )

async def setup(bot):
    await bot.add_cog(Moderation(bot))