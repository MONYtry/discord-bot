from discord.ext import commands
from config import BAN_CHANNEL_ID

class Log(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Log bereit")

    @commands.Cog.listener()
    async def on_member_ban(self,guild,user):
        channel = self.bot.get_channel(BAN_CHANNEL_ID)
        if channel is not None:
            helper_cog = self.bot.get_cog("Helper")
            await helper_cog.send_embed(
                channel,
                "Member was banned",
                f"🔨 **User gebannt!**\n"
                f"👤 User: {user.mention} (`{user.id}`)")
            print(f"Log: Member was banned, 👤 User: {user}")
    
    
async def setup(bot):
    await bot.add_cog(Log(bot))
    