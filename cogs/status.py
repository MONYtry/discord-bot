
import discord
from discord.ext import commands
from datetime import datetime
from config import STATUS_CHANNEL_ID

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.already_logged = False
        self.cleanup_done = False
        self.is_online = False
   

    @commands.Cog.listener()
    async def on_ready(self):
        if self.already_logged:
            return
                
        self.already_logged = True
        helper_cog = self.bot.get_cog("Helper")
        await helper_cog.logMessage("status.py","Succcsessfully loaded")

        self.is_online = True
        if self.cleanup_done:
            return
        
        channel = self.bot.get_channel(STATUS_CHANNEL_ID)
        if channel is not None:
            deleted = await channel.purge(limit=10)
            await helper_cog.logMessage("status.py",f"Succcsessfully cleart {channel} with {len(deleted)} messages")
            self.cleanup_done = True
            # Sendet den Status in den angegebenen Parameter
            await self.send_status(channel)

    async def send_status(self, channel):
        embed = discord.Embed(
            title="♨️ Bot-Status",
            description="Hier findest du den aktuellen Bot-Status.",
            timestamp=datetime.now().astimezone()
        )

        embed.color = (discord.Color.green() if self.is_online else discord.Color.red())
        
        status = "🟢 Online" if self.is_online else "🔴 Offline"
        
        embed.add_field(name="Status", value=status, inline=True)
        embed.add_field(name="Version", value="1.0 Beta", inline=True)
        embed.set_footer(text="Developer Academy Bot • Made with Love ❤️")
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        # Sendet den Embed
        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Status(bot))
