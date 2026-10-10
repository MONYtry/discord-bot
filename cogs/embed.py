import discord
from discord.ext import commands
from config import EMBED_ALLOWED_ROLE_IDS

# Erstellt eine Class mit Discord UI & Titel
class EmbedModal(discord.ui.Modal, title="Embed erstellen"):
    # Erstellung der Felder
    titel = discord.ui.TextInput(
        # Anzeige
        label="Titel",
        # Platzhalter
        placeholder="Gib den Titel ein ...",
        # Maximale Zeichen
        max_length=256
    )

    beschreibung = discord.ui.TextInput(
        label="Beschreibung",
        placeholder="Schreibe deinen Embed-Text ...",
        style=discord.TextStyle.paragraph,
        max_length=4000
    )

    footer = discord.ui.TextInput(
        label="Fußzeile",
        placeholder="Gebe den Inhalt deiner Fusszeile an...",
        style=discord.TextStyle.paragraph,
        max_length=100
    )

    # Sobald abgeschickt wird
    async def on_submit(self, interaction: discord.Interaction):
        # Embed wird erstellt
        embed = discord.Embed(
            # Setzt den eben erstellten Titel
            title=self.titel.value,
            # Setzt die eben erstellte Beschreibung 
            description=self.beschreibung.value,
            color=discord.Color.red()
        )
        # Fügt Fußzeile hinzu
        embed.set_footer(text=self.footer)
        
        # Sendet Antwort Nachricht
        await interaction.response.send_message("✅ Dein Embed wurde erstellt!",ephemeral=True)
        
        # Sendet in den Channel wo der Command ausgeführt wurde
        if interaction.channel:
            await interaction.channel.send(embed=embed)

class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Erstellt Command 
    @discord.app_commands.command(name="sendembed", description="Öffnet ein Formular zum Erstellen eines Embeds")
    async def sendembed(self, interaction: discord.Interaction):
        
        # Prüft ob der Nutzer eine Rolle hat welche Rechte dazu hat
        has_permission = any(role.id in EMBED_ALLOWED_ROLE_IDS for role in interaction.user.roles)
        if not has_permission:
            await interaction.response.send_message("Du hast dazu keine Rechte!", ephemeral=True)
            return
        # Sendet den PopUp
        await interaction.response.send_modal(EmbedModal())

async def setup(bot):
    await bot.add_cog(Embed(bot))
