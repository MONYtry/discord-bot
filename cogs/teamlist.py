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
            print(f"Guild: {guild.name} | ID: {guild.id}")

            pingRoles = get_role_id_list(guild.id, "supporting_roles")

            print(f"PingRoles: {pingRoles}")

            if not pingRoles:
                print("Es wurden keine Team-Rollen gefunden!")
                continue

            for role in pingRoles:
                print(f"Role: {role}")

            channel_id = get_value_channel(guild.id,"apply_channel_id")
            if channel_id is None:
                continue

            channel = self.bot.get_channel(channel_id)    
            if channel is None:
                continue
            
            text = []
            for role_id in pingRoles:
                role = guild.get_role(role_id)
                if role is not None:
                    text.append(role.mention)

            # Fügt einen Zeilenumbruch hinzu
            # .join macht aus einer Liste einen Vanilla String
            text = "\n".join(text)
            
            await helper_cog.send_embed(channel,"Team-Liste",text,discord.Color.red())
                

async def setup(bot):
    await bot.add_cog(Teamlist(bot))
    