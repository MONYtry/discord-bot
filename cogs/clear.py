
import discord
from discord.ext import commands

class Clear(commands.Cog):
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
        await helper_cog.logSuccess("clear.py","Succcsessfully loaded")

    # Regisitiert den Command
    @discord.app_commands.command(name="clear", description="Löscht Nachrichten")
    
    # Fügt den Amount Platzhalter hinzu & auch Beschreibung
    @discord.app_commands.describe(amount="Anzahl der Nachrichten (1–100)")
    async def clear(self, interaction: discord.Interaction, amount: discord.app_commands.Range[int, 1, 100]):
        helper_cog = self.bot.get_cog("Helper")
        if helper_cog is None:
            await interaction.response.send_message("Etwas ist schief gelaufen, bitte versuche es in kürze erneut!", ephemeral=True)
            return
                
        if not await helper_cog.get_permission(interaction, "admin_perm_roles"):
            return

        # Sagt das eine Aufgabe gestartet wurde
        await interaction.response.defer(ephemeral=True)
        
        # Löscht Nachrichten jenachdem was bei Limit definiert wurde
        deleted = await interaction.channel.purge(limit=amount)
        
        # Sobald Aufgabe erledigt ist <- Nachricht senden
        await interaction.followup.send(f"🗑️ {len(deleted)} Nachrichten gelöscht!", ephemeral=True)
            
async def setup(bot):
    await bot.add_cog(Clear(bot))
