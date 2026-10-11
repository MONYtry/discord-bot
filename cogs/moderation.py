import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

ID = 1557488290511196211
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation bereit")
    
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

        channel = self.bot.get_channel(ID)
        helper_cog = self.bot.get_cog("Helper")


        try:
            if user.is_timed_out():
                await user.timeout(None, reason="Timeout aufgegeben")
                await interaction.response.send_message(f"Timeout von {user} wurde aufgehoben", ephemeral=True)
                await helper_cog.send_embed(
                                    channel,
                                    "Member Timeout removed",
                                    f"🔨 **User timeout removed!**\n"
                                    f"👤 User: {user.mention} (`{user.id}`)\n"
                                )
                print("User wurde ist schon getimeouted <- untimeout!")
                return
            
            await user.timeout(dauer_zeit, reason=reason)

        except discord.Forbidden:
            await interaction.response.send_message("❌ Bot fehlen die nötigen Rechte!", ephemeral=True)
            return
        
        await interaction.response.send_message(f"{user} wurde getimeoutet für {duration} {timetype.name}", ephemeral=True)

        
        if channel:
            if helper_cog:
                await helper_cog.send_embed(
                    channel,
                    "Member was timedout",
                    f"🔨 **User timeoutet!**\n"
                    f"👤 User: {user.mention} (`{user.id}`)\n"
                    f"⏳ Dauer: {duration} {timetype.name}\n"
                    f"📝 Grund: {reason}"
                )

async def setup(bot):
    await bot.add_cog(Moderation(bot))