import discord
from discord.ext import commands
from config import (REACTION_ROLES_IDS, 
                    REMOVED_REACTION_ROLE_MESSAGE, 
                    ADDED_REACTION_ROLE_MESSAGE, 
                    SEND_DROPDOWN_ROLE_IDS,
                    NO_RIGHTS_MESSAGE, REACTION_ROLE_OPTIONS)

class RoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Reactionroles())

class DropDownReactionRoles(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Automoderation ist bereit")

    # Erstellt Command
    @discord.app_commands.command(name="senddropdown", description="Sendet ein Auswahlmenü für Rollen")
    async def senddropdown(self, interaction: discord.Interaction):

        # Prüft ob der Nutzer eine Rolle hat welche Rechte dazu hat
        has_permission = any(role.id in SEND_DROPDOWN_ROLE_IDS for role in interaction.user.roles)
                
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