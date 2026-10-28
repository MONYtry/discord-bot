from discord import app_commands
from datetime import timedelta
import asyncio
import discord
from discord.ext import commands


class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="timer", description="Startet einen Timer")
    @app_commands.describe(duration="Dauer des Timers", timetype="Minuten, Stunden oder Tage")
    
    @app_commands.choices(timetype=[
        app_commands.Choice(name="Minuten", value="minuten"),
        app_commands.Choice(name="Stunden", value="stunden"),
        app_commands.Choice(name="Tage", value="tage")
    ])
    async def timer(
        self,
        interaction: discord.Interaction,
        timetype: app_commands.Choice[str],
        duration: int,
        reason: str,
    ):
        helper_cog = self.bot.get_cog("Helper")
        if helper_cog is None:
            print("Helper_Cog wurde nicht richtig geladen")
            return
        
        time_units = {
            "minuten": timedelta(minutes=1),
            "stunden": timedelta(hours=1),
            "tage": timedelta(days=1)
        }

        # Null Reference vermeiden
        if duration < 1:
            await interaction.response.send_message("❌ Die Dauer muss mindestens 1 sein!", ephemeral=True)
            return
        
        # Zeit berechnung
        # Holt sich den Zeit-Typen und multipliziert ihn mal die Dauer
        dauer_zeit = time_units[timetype.value] * duration
        # Start Message an den User        
        await interaction.response.send_message(f"⏱️ Timer gestartet für **{duration} {timetype.name}**!",ephemeral=True)

        # Wartet für die angebene Zeit
        await asyncio.sleep(dauer_zeit.total_seconds())

        # Nachricht an den User 
        await interaction.followup.send(await helper_cog.send_embed(interaction.channel,"Timer abgelaufen",f"🔔 Hey {interaction.user.mention},\n dein Timer ist abgelaufen! \n Grund: {reason}", discord.Color.blue()))

async def setup(bot):
    await bot.add_cog(Timer(bot))