from discord.ext import commands
import discord
from config import MESSAGE_LOG_CHANNEL


class Automod(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.already_logged = False

    @commands.Cog.listener()
    async def on_ready(self):
        if self.already_logged:
            return
                
        self.already_logged = True
        helper_cog = self.bot.get_cog("Helper")
        await helper_cog.logMessage("Automod.py","Succcsessfully loaded")
    
    @commands.Cog.listener()
    async def on_message_delete(self,message):
        
        if message.author.bot: 
            return
        
        print(
            f"\n{'=' * 40}\n"
            f"👤 User: {message.author} (ID: {message.author.id})\n"
            f"📍 Channel: #{message.channel.name }\n"
            f"💬 Nachricht: {message.content}\n"
            f"🕒 Zeit: {message.created_at.strftime('%d.%m.%Y %H:%M:%S')} UTC\n"
            f"{'=' * 40}")

        # Holt sich die Module anhand der Class-Namen
        helper_cog = self.bot.get_cog("Helper")
        log_channel = self.bot.get_channel(MESSAGE_LOG_CHANNEL)
        if log_channel is not None:
            await helper_cog.send_embed(log_channel,"Message deleted",
                                        f"👤 User: {message.author.mention} (ID: {message.author.id})\n"
                                        f"📍 Channel: #{message.channel.mention}\n"
                                        f"💬 Nachricht: {message.content}\n"
                                        f"🕒 Zeit: {message.created_at.strftime('%d.%m.%Y %H:%M:%S')} UTC\n"
                                        ,discord.Color.red(), message.author.avatar.url)
            
    @commands.Cog.listener()
    async def on_message(self,message):
        
        if message.author.bot: 
            return
        
        print(
        # Schreibt x40 "="
        f"\n{'=' * 40}\n"
        f"👤 User: {message.author} (ID: {message.author.id})\n"
        f"📍 Channel: #{message.channel.name }\n"
        f"💬 Nachricht: {message.content}\n"
        f"🕒 Zeit: {message.created_at.strftime('%d.%m.%Y %H:%M:%S')} UTC\n"
        f"{'=' * 40}"
    )
        # Holt sich die Module anhand der Class-Namen
        helper_cog = self.bot.get_cog("Helper")
        log_channel = self.bot.get_channel(MESSAGE_LOG_CHANNEL)
        if log_channel is not None:
            await helper_cog.send_embed(log_channel,"Message send",
                                        f"👤 User: {message.author.mention} (ID: ||{message.author.id}||)\n"
                                        f"📍 Channel: #{message.channel.mention}\n"
                                        f"💬 Nachricht: {message.content}\n"
                                        f"🕒 Zeit: {message.created_at.strftime('%d.%m.%Y %H:%M:%S')} UTC\n"
                                        ,discord.Color.red(), message.author.avatar.url)

async def setup(bot):
    await bot.add_cog(Automod(bot))