
import discord
from discord.ext import commands
from config import BOT_STATUS_CHANNEL_ID, SERVER_ID, EMBED_ALLOWED_ROLE_IDS


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
        # Geht jede Rolle durch 
        has_permission = any(role.id in EMBED_ALLOWED_ROLE_IDS for role in interaction.user.roles)
        # Wenn der Nutzer keine Rechte hat
        if not has_permission:
            await interaction.response.send_message("Du hast dazu keine Rechte!", ephemeral=True)
            return
        
        # Bot wird ausgeschalten
        await interaction.response.send_message("🔴 Bot geht offline.", ephemeral=True)
        
        channel = self.bot.get_channel(BOT_STATUS_CHANNEL_ID)
        
        # Holt sich die Module anhand der Class-Namen
        status_cog = self.bot.get_cog("Status")
        clear_cog = self.bot.get_cog("Clear")
        helper_cog = self.bot.get_cog("Helper")

        # Räumt den Channel auf danach kommt der Embed
        if channel is not None and status_cog is not None:
            status_cog.is_online = False

            guild = self.bot.get_guild(SERVER_ID)
            await helper_cog.get_member_count(guild)
            
            await clear_cog.clear_channel(channel,10)
            await status_cog.send_status(channel)
        
        # Stoppt den Bot
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(Admin(bot))
