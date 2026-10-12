import discord
from discord.ext import commands
from datetime import datetime
from config import (WELCOME_CHANNEL_ID, 
                    WELCOME_MESSAGE, 
                    JOIN_LEAVE_LOG_CHANNEL,
                    JOIN_LOG_MESSAGE, 
                    JOIN_TITEL_LOG_MESSAGE,LEAVE_LOG_MESSAGE, LEAVE_TITEL_LOG_MESSAGE,WELCOME_THUMBNAIL_URL)


class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.already_logged = False

    @commands.Cog.listener()
    async def on_ready(self):
        if self.already_logged:
            return
                
        self.already_logged = True
        helper_cog = self.bot.get_cog("Helper")
        await helper_cog.logMessage("join.py","Succcsessfully loaded")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        log_channel = self.bot.get_channel(JOIN_LEAVE_LOG_CHANNEL)

        helper_cog = self.bot.get_cog("Helper")

        if log_channel is None:
            print("Kanal nicht gefunden!")
            return
        
        if channel is None:
            print("Kanal nicht gefunden!")
            return
        
        join_message = JOIN_LOG_MESSAGE.format(member=member.mention)
        await helper_cog.send_embed(log_channel,JOIN_TITEL_LOG_MESSAGE,join_message, discord.Color.green(), member.display_avatar.url)
        
        # Embed senden
        await self.send_embed(channel, member)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        log_channel = self.bot.get_channel(JOIN_LEAVE_LOG_CHANNEL)
    
        helper_cog = self.bot.get_cog("Helper")
    
        if log_channel is None:
            print("Kanal nicht gefunden!")
            return
            
        if channel is None:
            print("Kanal nicht gefunden!")
            return
        
        leave_message = LEAVE_LOG_MESSAGE.format(member=member.mention)
        await helper_cog.send_embed(log_channel,LEAVE_TITEL_LOG_MESSAGE, leave_message, discord.Color.red(), member.display_avatar.url)
    
    async def send_embed(self, channel, member):
        helper_cog = self.bot.get_cog("Helper")
        member_count = await helper_cog.get_member_count(member.guild)

        description = WELCOME_MESSAGE.format(member=member.mention)

        embed = discord.Embed(
            title="🎉 Welcome to the Server!",
            description=description,
            timestamp=datetime.now().astimezone(),
            color=discord.Color.red()
        ) 

        
        embed.set_footer(text=f"Developer Academy Bot • Made with Love ❤️ • #{member_count}")

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=WELCOME_THUMBNAIL_URL)

        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Join(bot))
