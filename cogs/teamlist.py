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
            pingRoles = get_role_id_list(guild.id, "team_roles")

            if not pingRoles:
                continue

            channel_id = get_value_channel(guild.id,"TEAMLIST_CHANNEL_ID")
            if channel_id is None:
                continue

            channel = self.bot.get_channel(channel_id)    
            if channel is None:
                continue

            text = []

            # Geht durch alle Rollen
            for role_id in pingRoles:
                
                role = guild.get_role(role_id)
                # Falls die Rolle nicht exisitiert
                if role is None:
                    continue

                users = []
                # Geht durch alle Nutzer der aktuellen Rolle
                for user in role.members:
                    users.append(user.mention)

                # Falls die Rolle keine Nutzer hat
                if not users:
                    users.append("*Keine Mitglieder*")
                
                # Fügt dem Array ein String hinzu
                text.append(f"# {role.mention} \n" + "\n".join(users))

            final_text = "\n\n".join(text)

            await helper_cog.send_embed(channel, "Team-Liste", final_text, discord.Color.red())

async def setup(bot):
    await bot.add_cog(Teamlist(bot))
    