
import discord
from discord.ext import commands
from config import NO_RIGHTS_MESSAGE
from api.database import get_value_channel, get_role_id_list

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
    @discord.app_commands.command(name="banlist", description="Gibt Liste von gebannten Nutzern")
    async def banlist(self, interaction: discord.Interaction):  
        guild = interaction.guild
        if guild is None:
            return

        bans = []
        text = ""

        async for i in guild.bans(limit=None):
            bans.append(i)
            text += f"• {i.user} (ID: {i.user.id})\n"

        if not bans:
            await interaction.response.send_message("Keine gebanntent Nutzer", ephemeral=True)

        # text[:1800] <- ersten 1800 Zeichen des Strings
        await interaction.response.send_message(
            f"🔨 **Gebannte Nutzer ({len(bans)}):**\n"
            f"```text\n{text[:1800]}\n```", ephemeral=True)

    @discord.app_commands.command(name="unbanall", description="Entbannt alle Nutzer")
    async def unban(self, interaction: discord.Interaction):
        guild = interaction.guild
        if guild is None:
            return

        await interaction.response.defer(ephemeral=True)

        member_id_bans = []

        async for i in guild.bans():
            user_id = i.user.id
            member_id_bans.append(user_id)

            user = await self.bot.fetch_user(int(user_id))
            await guild.unban(user)

        if member_id_bans:
            await interaction.followup.send(f"✅ Erfolgreich {len(member_id_bans)} entbannt!", ephemeral=True)
            member_id_bans.clear()
        else:
            await interaction.followup.send("Es wurden keine Mitglieder entbannt!", ephemeral=True)

    # Regisiterung von Command
    @discord.app_commands.command(name="shutdown", description="Fährt den Bot herunter")
    async def shutdown(self, interaction: discord.Interaction):    
        # Geht jede Rolle durch 
        admin_roles = get_role_id_list(interaction.guild.id,"admin_perm_roles")

        has_permission = False
        for role in interaction.user.roles:
            if role.id in admin_roles:
                has_permission = True
                break

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
