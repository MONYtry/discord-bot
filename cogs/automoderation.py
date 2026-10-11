from discord.ext import commands
import discord
from config import MESSAGE_LOG_CHANNEL


class Automod(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Automoderation ist bereit")
    
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
        channel = self.bot.get_channel(MESSAGE_LOG_CHANNEL)
        if channel is not None:
            await helper_cog.send_embed(channel,"Message was deleted",message.content,discord.Color.red())
            
    @commands.Cog.listener()
    async def on_message(self,message):
        
        if message.author.bot: 
            return
        
        print(
        f"\n{'=' * 40}\n"
        f"👤 User: {message.author} (ID: {message.author.id})\n"
        f"📍 Channel: #{message.channel.name }\n"
        f"💬 Nachricht: {message.content}\n"
        f"🕒 Zeit: {message.created_at.strftime('%d.%m.%Y %H:%M:%S')} UTC\n"
        f"{'=' * 40}"
    )
        # Holt sich die Module anhand der Class-Namen
        helper_cog = self.bot.get_cog("Helper")
        channel = self.bot.get_channel(MESSAGE_LOG_CHANNEL)
        if channel is not None:
            await helper_cog.send_embed(channel,"Message was send",message.content,discord.Color.yellow())


async def setup(bot):
    await bot.add_cog(Automod(bot))