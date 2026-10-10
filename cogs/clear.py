
import discord
from discord.ext import commands
from config import EMBED_ALLOWED_ROLE_IDS

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Sobald das Modul geladen wird
    @commands.Cog.listener()
    async def on_ready(self):
        print("Clear-Modul bereit!")

    # Regisitiert den Command
    @discord.app_commands.command(name="clear", description="Löscht Nachrichten")
    
    # Fügt den Amount Platzhalter hinzu & auch Beschreibung
    @discord.app_commands.describe(amount="Anzahl der Nachrichten (1–100)")
    async def clear(
        self,
        interaction: discord.Interaction,
        amount: discord.app_commands.Range[int, 1, 100]):

        # Prüft ob der Nutzer eine Rolle hat welche Rechte dazu hat
        has_permission = any(role.id in EMBED_ALLOWED_ROLE_IDS for role in interaction.user.roles)
        if not has_permission:
            await interaction.response.send_message("Keine Rechte!", ephemeral=True)
            return

        # Sagt das eine Aufgabe gestartet wurde
        await interaction.response.defer(ephemeral=True)
        
        # Löscht Nachrichten jenachdem was bei Limit definiert wurde
        deleted = await interaction.channel.purge(limit=amount)
        
        # Sobald Aufgabe erledigt ist <- Nachricht senden
        await interaction.followup.send(f"🗑️ {len(deleted)} Nachrichten gelöscht!", ephemeral=True)

    async def clear_channel(self,channel, amount):
        if channel is not None:
            try:
                deleted = await channel.purge(limit=amount)
                print(f"Es wurden {len(deleted)}-Nachrichten gelöscht!")
            except:
                print("Fehler :|")
            
async def setup(bot):
    await bot.add_cog(Clear(bot))
