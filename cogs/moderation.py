import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

from config import NO_RIGHTS_MESSAGE,SUPPORT_THUMBNAIL_URL
from api.database import get_value_channel, get_role_id_list

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
        await helper_cog.logSuccess("moderation.py","Succcsessfully loaded")
    
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
        
        TIMEOUT_ALLOWED_ROLE_IDS = get_role_id_list(interaction.guild.id,"supporting_roles")
        if TIMEOUT_ALLOWED_ROLE_IDS is None:
            await interaction.response.send_message("Es ist ein kritischer interner Fehler aufgetreten! (Kontaktiere einen Admin)")
            return
        
        has_permission = False

        for role in interaction.user.roles:
             if role.id in TIMEOUT_ALLOWED_ROLE_IDS:
                has_permission = True
                break

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
        channel_id = get_value_channel(interaction.guild_id, "TIMEOUT_LOG_CHANNEL")
        
        if channel_id is None:
            await interaction.response.send_message("Es wurde kein Log-Channel-ID für Timeout gefunden! (Kontaktiere einen Admin)", ephemeral=True)
            return
        
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            await interaction.response.send_message("Es wurde kein Log-Channel für Timeout gefunden! (Kontaktiere einen Admin)", ephemeral=True)
            return
        
        helper_cog = self.bot.get_cog("Helper")
        if helper_cog is None:
            await interaction.response.send_message("Etwas ist schief gelaufen, bitte versuche es in kürze erneut!", ephemeral=True)
            return
        
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
                f"Details: {e.text}", ephemeral=True)
            return
        
        await interaction.response.send_message(f"{user.mention} wurde getimeoutet für {duration} {timetype.name}", ephemeral=True)

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