from discord.ext import commands
import discord
from config import (
                    SUPPORT_THUMBNAIL_URL,
                    FORBIDDEN_WORDS, 
                    BOT_HAS_NO_RIGHTS,
                    TRUSTED_URL)
from datetime import timedelta
from api.database import get_message_log_channel

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
        await helper_cog.logSuccess("Automod.py","Succcsessfully loaded")
    
    @commands.Cog.listener()
    async def on_message_delete(self,message):
        
        if message.author.bot: 
            return

        # Holt sich die Module anhand der Class-Namen
        helper_cog = self.bot.get_cog("Helper")
        channel_id = get_message_log_channel(message.guild.id)
        print(f"Automoderation: {channel_id}")
        log_channel = self.bot.get_channel(channel_id)
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
        
        # Holt sich die Module anhand der Class-Namen
        helper_cog = self.bot.get_cog("Helper")
        channel_id = get_message_log_channel(message.guild.id)
        print(f"Automoderation: {channel_id}")
        log_channel = self.bot.get_channel(channel_id)
        
        if log_channel is not None:
            if await self.checkForbiddenWords(message,helper_cog,log_channel):
                return
            if await self.checkForbiddenLinks(message,helper_cog,log_channel):
                return
            
            await helper_cog.logMessage("automod.py",
                    # Schreibt x40 "="
                    f"\n{'=' * 40}\n"
                    f"👤 User: {message.author} (ID: {message.author.id})\n"
                    f"📍 Channel: #{message.channel.name }\n"
                    f"💬 Nachricht: {message.content}\n"
                    f"🕒 Zeit: {message.created_at.strftime('%d.%m.%Y %H:%M:%S')} UTC\n"
                    f"{'=' * 40}"
                )
            
            await helper_cog.send_embed(log_channel,"Message send",
                                        f"👤 User: {message.author.mention} (ID: ||{message.author.id}||)\n"
                                        f"📍 Channel: #{message.channel.mention}\n"
                                        f"💬 Nachricht: {message.content}\n"
                                        f"🕒 Zeit: {message.created_at.strftime('%d.%m.%Y %H:%M:%S')} UTC\n"
                                        ,discord.Color.red(), message.author.avatar.url)
        await self.checkForbiddenWords(message,helper_cog,log_channel)
        await self.checkForbiddenLinks(message,helper_cog,log_channel)

    async def checkForbiddenWords(self,message,helper_cog,channel):
        # Hilfs Variablen
        content = message.content.lower()
        # Leert den Array
        found_words = []

        for word in FORBIDDEN_WORDS:
            if word.lower() in content:
                found_words.append(word)
        # Falls Wort gefunden wird
        if found_words:
            await helper_cog.logMessage("automod.py",
                        f"⚠️ Blacklist-Wörter erkannt: {found_words}\n"
                        f"👤 User: {message.author} ({message.author.id})\n"
                        f"📍 Channel: #{message.channel}\n"
                        f"💬 Nachricht: {message.content}")
            
            # Löscht Nachricht
            await message.delete()
            
            # Timeoutet User
            await self.timeout(message,helper_cog)
            
            # Sendet Privat Message
            await self.handleModerationMessage(message,found_words)

            if channel is not None:
                await helper_cog.send_embed(channel, "Bad word",  
                                            f"👤 User: {message.author.mention} ||{message.author.id}|| \n"
                                            f"💬 Nachricht: {message.content} \n"
                                            f"📍Channel: #{message.channel.mention} \n"
                                            f"🕒 Zeit: {message.created_at.strftime('%d.%m.%Y %H:%M:%S')} UTC\n"
                                            ,discord.Color.red(),message.author.avatar.url)
            return True
        return False
    
    

    async def checkForbiddenLinks(self, message, helper_cog, channel):
            # Hilfs-Variable
            content = message.content.lower()
            # Falls in der URL eine Trusted URL steckt, abbruch
            for url in TRUSTED_URL:
                if url.lower() in content:
                    return False
    
            # Wenn ein Link enthalten ist
            if "https://" in content or "http://" in content:
                # Löscht Nachricht
                await message.delete()
                # Sendet private Nachricht
                await self.handleModerationMessage(message,message.content)
                # Timeoutet User
                await self.timeout(message,helper_cog)
                # 
                return True
            return False
    
    async def handleModerationMessage(self,message,list):
        await message.author.send(f"{message.author.mention}")
        embed = discord.Embed(
                                # Setzt den eben erstellten Titel
                                title="🛡️ AUTO-MOD",
                                # Setzt die eben erstellte Beschreibung 
                                description="⚠️ Deine Nachricht wurde gelöscht!",
                                color=discord.Color.red())

        embed.add_field(name="Grund:",value=f"Unerwünschter Inhalt: {list}", inline=True)
        embed.add_field(name="Hinweis:",value=f"Bitte Verhalte dich in Zukunft besser,\n damit weitere Schritte nicht nötig sind",inline=True)
        embed.set_image(url=SUPPORT_THUMBNAIL_URL)
        embed.set_thumbnail(url=message.author.avatar.url)
        embed.set_footer(text="Developer Academy Bot • Made with Love ❤️")

        await message.author.send(embed=embed)

    async def timeout(self,message,helper_cog):
        # Fehler vermeidung
        try:
            # Sendet User in den Timeout
            await message.author.timeout(timedelta(minutes=5), reason="Unerwünschter Inhalt!")
        # Falls User höhere Rechte hat als Bot
        except discord.Forbidden:
            await helper_cog.logMessage("Automod.py",BOT_HAS_NO_RIGHTS)
            
async def setup(bot):
    await bot.add_cog(Automod(bot))