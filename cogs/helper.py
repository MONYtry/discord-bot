from discord.ext import commands

class Helper(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    async def get_member_count(self, guild):
        return guild.member_count


async def setup(bot):
    await bot.add_cog(Helper(bot))
