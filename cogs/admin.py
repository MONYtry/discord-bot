
import discord
from discord.ext import commands
from config import NO_RIGHTS_MESSAGE
from api.database import get_value_channel, get_admin_perm_roles

class Admin(commands.Cog):
    # Wird direkt aufgerufen
    def __init__(self, bot):
        self.bot = bot
        self.already_logged = False

    # Sobald das Modul geladen wird
    @commands.Cog.listener()
    async def on_ready(self):
        if self.already_logged:
            return
                
        self.already_logged = True
        helper_cog = self.bot.get_cog("Helper")
        await helper_cog.logSuccess("Admin.py","Succcsessfully loaded")

    # Regisiterung von Command
    @discord.app_commands.command(name="shutdown", description="Fährt den Bot herunter")
    async def shutdown(self, interaction: discord.Interaction):    
        # Geht jede Rolle durch 
        admin_roles = get_admin_perm_roles(interaction.guild.id)

        has_permission = any(
            role.id in admin_roles
            for role in interaction.user.roles
        )
        
        # Wenn der Nutzer keine Rechte hat
        if not has_permission:
            await interaction.response.send_message(NO_RIGHTS_MESSAGE, ephemeral=True)
            return
        
        # Holt sich die Module anhand der Class-Namen
        status_cog = self.bot.get_cog("Status")
        clear_cog = self.bot.get_cog("Clear")
        helper_cog = self.bot.get_cog("Helper")
        
        if status_cog is None or clear_cog is None or helper_cog is None:
            await helper_cog.logMessage("admin.py","Es ist ein Fehler bei dem Laden der Hilfs-Modulen aufgetreten")
            await interaction.response.send_message("Es ist ein interner Fehler aufgetreten (Kontaktiere einen Admin)")
            return
        
        # Bot wird ausgeschalten
        await interaction.response.send_message("🔴 Bot geht offline.", ephemeral=True)

        channel_id = get_value_channel(interaction.guild.id, "BOT_STATUS_CHANNEL_ID")
        if channel_id is None:
            print("Keine Id gefunden zum shutdownen!")
            return
        
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            print(f"Fehler Channel: {channel} wurde nicht gefunden (None)")
            return
        
        

        # Räumt den Channel auf danach kommt der Embed
        if channel is not None and status_cog is not None:
            status_cog.is_online = False

            guild = self.bot.get_guild(interaction.guild.id)
            await helper_cog.get_member_count(guild)
            
            await clear_cog.clear_channel(channel,10)
            await status_cog.send_status(channel)
        
        # Stoppt den Bot
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(Admin(bot))
