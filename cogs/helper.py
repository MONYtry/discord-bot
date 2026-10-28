from discord.ext import commands
import discord
import datetime
from api.main import get_role_id_list
from config import NO_RIGHTS_MESSAGE

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

    async def get_permission(self,interaction, role_perm):
        # Geht jede Rolle durch 
        admin_roles = get_role_id_list(interaction.guild.id,role_perm)
        
        if admin_roles is None:
            return False
        
        for role in interaction.user.roles:
            if role.id in admin_roles:
                return True

        # Wenn der Nutzer keine Rechte hat
        await interaction.response.send_message(NO_RIGHTS_MESSAGE, ephemeral=True)
        return False

    async def logError(self,fileName,message):
        RED = "\033[91m"
        BLUE = "\033[94m"
        RESET = "\033[0m"

        print(f"{BLUE}[{datetime.datetime.now()}]{RESET} |{RED} [ERROR] {RESET}   at {fileName}, {message}")
    
    async def logMessage(self,fileName,message):
        BLUE = "\033[94m"
        RESET = "\033[0m"

        print(f"{BLUE}[{datetime.datetime.now()}]{RESET} | [INFO]     at {fileName}, {message}")

    async def logSuccess(self,fileName,message):
            GREEN = "\033[92m"
            BLUE = "\033[94m"
            RESET = "\033[0m"

            print(f"{BLUE}[{datetime.datetime.now()}]{RESET} | {GREEN}[SUCCESS] {RESET} at {fileName}, {message}")

async def setup(bot):
    await bot.add_cog(Helper(bot))
