from discord.ext import commands
from api.database import get_ban_log_channel

class Log(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.already_logged = False

    @commands.Cog.listener()
    async def on_ready(self):    
        if self.already_logged:
            return
        
        self.already_logged = True
        helper_cog = self.bot.get_cog("Helper")
        await helper_cog.logMessage("log.py","Succcsessfully loaded")
        
    @commands.Cog.listener()
    async def on_member_ban(self,guild,user):
        channel_id = get_ban_log_channel(guild.id)
        channel = self.bot.get_channel(channel_id)
        
        if channel is not None:
            helper_cog = self.bot.get_cog("Helper")
            await helper_cog.send_embed(
                channel,
                "Member was banned",
                f"🔨 **User gebannt!**\n"
                f"👤 User: {user.mention} (`{user.id}`)", None)
            print(f"Log: Member was banned, 👤 User: {user}")

async def setup(bot):
    await bot.add_cog(Log(bot))
    