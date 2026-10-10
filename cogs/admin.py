
import discord
from discord.ext import commands

STATUS_CHANNEL_ID = 1558243145836269568


class Admin(commands.Cog):
    # Wird direkt aufgerufen
    def __init__(self, bot):
        self.bot = bot

        # Sobald das Modul geladen wird
    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin-Modul bereit!")

    # Regisiterung von Command
    @discord.app_commands.command(name="shutdown", description="Fährt den Bot herunter")

    async def shutdown(self, interaction: discord.Interaction):
        
        # Wenn der Nutzer kein Inhaber ist
        if not await self.bot.is_owner(interaction.user):
            await interaction.response.send_message("Du hast dazu keine Rechte!", ephemeral=True)
            return
        
        # Bot wird ausgeschalten
        await interaction.response.send_message("🔴 Bot geht offline.", ephemeral=True)
        
        channel = self.bot.get_channel(STATUS_CHANNEL_ID)
        # Holt sich die Module anhand der Class-Namen
        status_cog = self.bot.get_cog("Status")
        clear_cog = self.bot.get_cog("Clear")

        # Räumt den Channel auf danach kommt der Embed
        if channel is not None and status_cog is not None:
            status_cog.is_online = False
            await clear_cog.clear_channel(channel,10)
            await status_cog.send_status(channel)
        # Stoppt den Bot
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(Admin(bot))
