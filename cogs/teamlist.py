from discord.ext import commands
import discord
from api.database import get_value_channel, get_role_id_list

class Teamlist(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.already_logged = False

    @commands.Cog.listener()
    async def on_ready(self):    
        if self.already_logged:
            return
        
        self.already_logged = True
        helper_cog = self.bot.get_cog("Helper")
        await helper_cog.logSuccess("Teamlist.py","Succcsessfully loaded")
        
        for guild in self.bot.guilds:
            channel_id = get_value_channel(guild.id,"TEAMLIST_CHANNEL_ID")    
            if channel_id is None:
                return
            
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                return
            await channel.purge(limit=10)

            text = await self.create_teamList(guild)
            await helper_cog.send_embed(channel, "Team-Liste", text, discord.Color.red())

    
    @discord.app_commands.command(name="teamlist", description="Sendet ein Auswahlmenü für Rollen")
    async def teamlist(self, interaction: discord.Interaction):
        
        helper_cog = self.bot.get_cog("Helper")
        if helper_cog is None:
            await interaction.response.send_message("Etwas ist schief gelaufen, bitte versuche es in kürze erneut!", ephemeral=True)
            return
        
        # Falls User keine Rechte hat    
        if not await helper_cog.get_permission(interaction, "admin_perm_roles"):
            return
        
        channel_id = get_value_channel(interaction.guild.id,"TEAMLIST_CHANNEL_ID")    
        if channel_id is None:
            return
            
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            return
        await channel.purge(limit=10)
        text = await self.create_teamList(interaction.guild)

        await helper_cog.send_embed(channel, "Team-Liste", text, discord.Color.red())
        await interaction.response.send_message("Team-Liste wurde erfolgreich aktualisiert!", ephemeral=True)
        
    async def create_teamList(self, guild):
        helper_cog = self.bot.get_cog("Helper")
        if helper_cog is None:
            return ""

        pingRoles = get_role_id_list(guild.id, "team_roles")

        if not pingRoles:
            return "Keine Team-Rollen gefunden."

        text = []
        # Geht durch alle Rollen die gepingt werden sollen
        for role_id in pingRoles:
            role = guild.get_role(role_id)

            if role is None:
                continue

            users = []

            for user in role.members:
                users.append(user.mention)

            if not users:
                users.append("*Keine Mitglieder*")
            text.append(f"# {role.mention}\n" + "\n".join(users))

        return "\n\n".join(text)

async def setup(bot):
    await bot.add_cog(Teamlist(bot))
    