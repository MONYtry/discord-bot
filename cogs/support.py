from discord.ext import commands
import discord
from config import SUPPORT_CATEGORIES_OPTIONS
import asyncio

class SupportView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SupportCategories())

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    #  Erstellt Button
    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="🔒")
    async def close_ticket(self,interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Ticket wird in demnächst gelöscht!", ephemeral=True)
        # Wartet 3 Sekunden
        await asyncio.sleep(3)
        # Löscht den Channel
        await interaction.channel.delete()
        

class SupportCategories(discord.ui.Select):
    def __init__(self):
        # Setzt Options
        options = [
            discord.SelectOption(label=data["label"], emoji=data["emoji"], value=key)
            # Geht durch alle SUPPORT_CATEGORIES_OPTIONS  
            for key, data in SUPPORT_CATEGORIES_OPTIONS.items()
        ]
        # Setzt Dropdown Settings
        super().__init__(
            placeholder="Wähle ein Ticket aus!",
            options=options,
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        # Hilfs-Variablen
        guild = interaction.guild
        member = interaction.user
        helper_cog = interaction.client.get_cog("Helper")
        
        selected_value = self.values[0]
        data = SUPPORT_CATEGORIES_OPTIONS[selected_value]

        TICKET_NAME = f"ticket-{member.id}-{data['label']}"
        
        # Durchsucht alle Kategorien nach (name="")
        category = discord.utils.get(guild.categories, name="Tickets")
        
        # Falls Kategorie nicht gefunden wurde
        if category is None:
            await interaction.response.send_message("Kategorie nicht gefunden!", ephemeral=True)
            return
        
        # Sucht nach Ticket
        ticket = discord.utils.get(guild.text_channels, name=TICKET_NAME)  
        if ticket is not None:
            await interaction.response.send_message(f"{member.mention} du hast bereits ein Ticket erstellt: {ticket.mention}", ephemeral=True)
            return
        
        # Erstellt einen Text-Channel
        channel = await guild.create_text_channel(
            # Setzt den Namen des Channels
            name=TICKET_NAME,
            # Setzt die Category
            category=category,
            
            # Überschreibt Rechte
            overwrites={
                # Überschreibt die Rechte des @Everyones (Niemand sieht diesen Channel)
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                # Nun sieht member diesen Channel
                member: discord.PermissionOverwrite(view_channel=True,send_messages=True)
            }
        )

        # MESSAGES IN NEW CHANNEL
        await channel.send(f"Willkommen {member.mention}!")
        await interaction.response.send_message(f"Ticket erstellt: {channel.mention}", ephemeral=True)
        
        
        
        # Erstellung von Embed Objekt & sendung
        await helper_cog.send_embed(
            channel,
            "Willkommen",
            "Unser Team wird sich zeitnah melden, bitte habe Geduld!",
            discord.Color.green())
        
        # Sendet Button
        await channel.send(view=TicketView())

class DropDown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="sendsupport", description="Sendet das Ticket-Menü")
    async def senddropdown(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=SupportView())


async def setup(bot):
    await bot.add_cog(DropDown(bot))