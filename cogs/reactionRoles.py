import discord
from discord.ext import commands
from config import (REACTION_ROLES_IDS, 
                    REMOVED_REACTION_ROLE_MESSAGE, 
                    ADDED_REACTION_ROLE_MESSAGE, 
                    NO_RIGHTS_MESSAGE, REACTION_ROLE_OPTIONS)
from api.database import get_role_id_list

class RoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Reactionroles())

class DropDownReactionRoles(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.already_logged = False
    
    @commands.Cog.listener()
    async def on_ready(self):
        if self.already_logged:
            return
                
        self.already_logged = True
        helper_cog = self.bot.get_cog("Helper")
        await helper_cog.logSuccess("reactionroles.py","Succcsessfully loaded")

    # Erstellt Command
    @discord.app_commands.command(name="senddropdown", description="Sendet ein Auswahlmenü für Rollen")
    async def senddropdown(self, interaction: discord.Interaction):

        team_roles = []
        role_ids = get_role_id_list(interaction.guild_id,"supporting_roles")
        if role_ids is None:
            print("Es wurden keine Rollen gefunden reactionroles.py")
        # Geht durch jede Rolle die in Support eingetragen ist 
        for role_id in role_ids:
            # Holt sich die Rolle
            role = interaction.guild.get_role(role_id)

            # Falls Rolle exsitiert
            if role is not None:
                team_roles.append(role)

        if not team_roles:
            await interaction.response.send_message("Es ist ein Fehler beim erstellen des Tickets aufgetreten!", ephemeral=True)
            return
        
        # Prüft ob der Nutzer eine Rolle hat welche Rechte dazu hat
        has_permission = any(role.id in get_role_id_list(interaction.guild_id,"admin_perm_roles") for role in interaction.user.roles)
                
        if not has_permission:
            await interaction.response.send_message(NO_RIGHTS_MESSAGE, ephemeral=True)
            return
        
        await interaction.response.send_message(view=RoleView())

    
class Reactionroles(discord.ui.Select):
    def __init__(self):
        # Erstellt Auswahlmöglichkeiten
        options = [
            discord.SelectOption(label=data["label"], emoji=data["emoji"], value=key)
            for key, data in REACTION_ROLE_OPTIONS.items()
        ]

        # Inistialisiert das Dropdown
        super().__init__(
            # Setzt Platzhalter
            placeholder="Wähle eine Rolle aus!",
            # Setzt die verfügbaren Optionen 
            options=options,
            # Mindestens & Maximal eine Auswahl
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        # Holt sich die Rollen und ihre ID
        roles = REACTION_ROLES_IDS

        # Versucht die Rolle zu finden
        role_id = roles.get(self.values[0])

        if role_id is None:
            print(f"Keine Rollen-ID für diese Auswahl gefunden! [#{role_id}]")
            return

        role = interaction.guild.get_role(int(role_id))

        if role is None:
            print(f"Rolle existiert nicht auf diesem Server! [#{role}]")
            return
        
        # Formatiert den Inhalt der Variable
        removed_message = REMOVED_REACTION_ROLE_MESSAGE.format(role=role.mention)
        added_message = ADDED_REACTION_ROLE_MESSAGE.format(role=role.mention)
        
        # Prüft ob Nutzer die Rolle bereits hat
        if interaction.user.get_role(roles[self.values[0]]):
            print("Nutzer hat die Rolle bereits! <- Rolle wird entfernt")
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(removed_message, ephemeral=True)
            return
        
        # Fügt die Rolle dem Nutzer hinzu
        await interaction.user.add_roles(role)
        # Schickt dem Nutzer eine bestätigungs Nachricht!
        await interaction.response.send_message(added_message, ephemeral=True)


async def setup(bot):
    await bot.add_cog(DropDownReactionRoles(bot))