import discord
from discord.ext import commands
from datetime import datetime
from config import WELCOME_CHANNEL_ID


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

        if channel is None:
            print("Kanal nicht gefunden!")
            return

        # Embed senden
        await self.send_embed(channel, member)

        print(f"Willkommensnachricht für {member} gesendet!")

    async def send_embed(self, channel, member):
        helper_cog = self.bot.get_cog("Helper")
        member_count = await helper_cog.get_member_count(member.guild)

        embed = discord.Embed(
            title="🎉 Welcome to the Server!",
            description=(
                f"Hey {member.mention}, welcome to our community💖\n\n"
                "We're happy to have you here! 🥳\n\n"
                "📜 **Before you get started, please read the server rules carefully.**\n"
                "They help keep our community friendly, safe, and fun for everyone.\n\n"
                "💬 Feel free to chat with other members, join the conversations, "
                "and have a great time!\n\n"
                "✨ **Make yourself at home and enjoy your stay!**"
            ),
            timestamp=datetime.now().astimezone(),
            color=discord.Color.red()
        ) 
        
        embed.set_footer(text=f"Developer Academy Bot • Made with Love ❤️ • #{member_count}")

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1534607507023069346/1558267347754819604/ChatGPT_Image_7._Okt._2026_22_52_37.png?ex=6acb79ce&is=6aca284e&hm=0de4a6795de0d0aac3dfdf51a42de9da2db6fba0124e976beaebab83c6182e6c&")

        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Join(bot))
