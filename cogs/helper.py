from discord.ext import commands
import discord
import datetime

class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.already_logged = False

    # Gets the Membercount
    async def get_member_count(self, guild):
        return guild.member_count

    # Embed Sending Method
    async def send_embed(self, channel,titel,message,color,url=None,urlThumbnail=None):
        embed = discord.Embed(
            title=titel,
            description=message,
            timestamp=datetime.datetime.now().astimezone(),
            color=color
            )
        if url is not None:
            embed.set_thumbnail(url=url)
        if urlThumbnail is not None:
            embed.set_image(url=urlThumbnail)

        # Sends the Embed in the Channel
        await channel.send(embed=embed)


    async def logError(self,fileName,message):
        print(f"[{datetime.datetime.now()}] | [ERROR] at {fileName}, {message}")
    
    async def logMessage(self,fileName,message):
        print(f"[{datetime.datetime.now()}] | [INFO] at {fileName}, {message}")

async def setup(bot):
    await bot.add_cog(Helper(bot))
