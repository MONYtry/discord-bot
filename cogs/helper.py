from discord.ext import commands
import discord
import datetime

class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Gets the Membercount
    async def get_member_count(self, guild):
        return guild.member_count

    # Embed Sending Method
    async def send_embed(self, channel,titel,message):
        embed = discord.Embed(
            title=titel,
            description=message,
            timestamp=datetime.datetime.now().astimezone(),
            color=discord.Color.red()
        )
        
        # Sends the Embed in the Channel
        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Helper(bot))
