import discord
from discord.ext import commands
from config import NO_RIGHTS_MESSAGE
from api.database import get_role_id_list

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
        max_length=100,
        required=False
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
        
        # Wenn keine Fußzeile angegeben wurde
        if not self.footer.value:
            footer_text = "Developer Academy Bot • Made with Love ❤️"
        else:
            footer_text = self.footer.value
        
        # Fügt Fußzeile hinzu
        embed.set_footer(text=footer_text)
        
        # Sendet Antwort Nachricht
        await interaction.response.send_message("✅ Dein Embed wurde erstellt!",ephemeral=True)
        
        # Sendet in den Channel wo der Command ausgeführt wurde
        if interaction.channel:
            await interaction.channel.send(embed=embed)

class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.already_logged = False

    @commands.Cog.listener()
    async def on_ready(self):
        if self.already_logged:
            return

        self.already_logged = True
        helper_cog = self.bot.get_cog("Helper")
        await helper_cog.logSuccess("embed.py","Succcsessfully loaded") 

    # Erstellt Command 
    @discord.app_commands.command(name="sendembed", description="Öffnet ein Formular zum Erstellen eines Embeds")
    async def sendembed(self, interaction: discord.Interaction):
        helper_cog = self.bot.get_cog("Helper")
        if helper_cog is None:
            print("Helpercog wasn't found embed.py")

        # Setzt Leere Rolle 
        team_roles = []
        role_ids = get_role_id_list(interaction.guild_id,"supporting_roles")

        # Geht durch jede Rolle die in Support eingetragen ist 
        for role_id in role_ids:
            # Holt sich die Rolle
            role = interaction.guild.get_role(role_id)
            await helper_cog.logMessage("embed.py",f"{interaction.guild.name} Role ID: {role_id} | Role: {role}")
                    
            # Falls Rolle exsitiert
            if role is not None:
                team_roles.append(role)

        if not team_roles:
            await helper_cog.logError("support.py","roles wasn't found!")
            await interaction.response.send_message("Es ist ein Fehler beim erstellen des Tickets aufgetreten!", ephemeral=True)
            return
        
        # Prüft ob der Nutzer eine Rolle hat welche Rechte dazu hat
        has_permission = any(role.id in get_role_id_list(interaction.guild_id,"embed_allowed_roles") for role in interaction.user.roles)
        if not has_permission:
            await interaction.response.send_message(NO_RIGHTS_MESSAGE, ephemeral=True)
            return
        # Sendet den PopUp
        await interaction.response.send_modal(EmbedModal())

async def setup(bot):
    await bot.add_cog(Embed(bot))
