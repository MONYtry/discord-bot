from discord.ext import commands
import discord
from config import SUPPORT_CATEGORIES_OPTIONS


class SupportView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SupportCategories())

class SupportCategories(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=data["label"], emoji=data["emoji"], value=key)
            for key, data in SUPPORT_CATEGORIES_OPTIONS.items()
        ]

        super().__init__(
            placeholder="Wähle ein Ticket aus!",
            options=options,
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user

        category = discord.utils.get(guild.categories, name="Tickets")

        if category is None:
            await interaction.response.send_message("Kategorie nicht gefunden!", ephemeral=True)
            return

        channel = await guild.create_text_channel(
            name=f"ticket-{member.id}",
            category=category,
            # Überschreibt Rechte
            overwrites={
                # Überschreibt die Rechte des @Everyones (Niemand sieht diesen Channel)
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                # Nun sieht member diesen Channel
                member: discord.PermissionOverwrite(view_channel=True,send_messages=True)
            }
        )

        await channel.send(f"Willkommen {member.mention}!")
        await interaction.response.send_message(f"Ticket erstellt: {channel.mention}", ephemeral=True)


class DropDown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="sendsupport", description="Sendet das Ticket-Menü")
    async def senddropdown(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=SupportView())


async def setup(bot):
    await bot.add_cog(DropDown(bot))