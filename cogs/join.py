import discord
from discord.ext import commands
from datetime import datetime
from config import (WELCOME_MESSAGE, 
                    JOIN_LOG_MESSAGE, 
                    JOIN_TITEL_LOG_MESSAGE,LEAVE_LOG_MESSAGE, LEAVE_TITEL_LOG_MESSAGE,WELCOME_THUMBNAIL_URL)
from api.database import get_welcome_channel, get_leave_join_log_channel

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
        await helper_cog.logSuccess("join.py","Succcsessfully loaded")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        helper_cog = self.bot.get_cog("Helper")
        if helper_cog is None:
            print("Helper_Cog wurde nicht richtig geladen")

        try:
            channel_id = get_welcome_channel(member.guild.id)
        except Exception as e:
            await helper_cog.logError("join.py",f"Fehler: {e}")
            return

        channel = self.bot.get_channel(int(channel_id)) if channel_id else None

        if channel is None:
            await helper_cog.logError("join.py",f"Fehler, welcome channel wasn't found!")
            return

        await self.send_embed(channel, member)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        helper_cog = self.bot.get_cog("Helper")
        try:
            join_leave_channel_id = get_leave_join_log_channel(member.guild.id)
        except Exception as e:
            await helper_cog.logError("join.py",f"FEHLER bei get_welcome_channel: {e}")
            return
        log_channel = self.bot.get_channel(join_leave_channel_id)
    
        helper_cog = self.bot.get_cog("Helper")
    
        if log_channel is None:
            await helper_cog.logError("join.py",f"FEHLER, Kanal nicht gefunden!")
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
