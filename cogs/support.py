from discord.ext import commands
import discord
import asyncio
import datetime
from config import (SUPPORT_CATEGORIES_OPTIONS,  
                    SUPPORT_EMBED_TITEL, 
                    SUPPORT_EMBED_MESSAGE,
                    SUPPORT_PREVIEW_EMBED_MESSAGE,
                    SUPPORT_PREVIEW_EMBED_TITEL,
                    SUPPORT_THUMBNAIL_URL)

from api.database import get_support_channel_id,get_support_channel_log,get_support_roles

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
        
        # Holt sich den Namen des Tickets
        channel_name = interaction.channel.name

        helper_cog = interaction.client.get_cog("Helper")

        # Holt sich die UserID anhand des Ticket-Name
        # z.B ticket-123-bug -> ticket 123 bug -> user_id = 123
        user_id = int(channel_name.split("-")[1])
        typ = str(channel_name.split("-")[2])

        # Erstellt Member-Object anhand der UserID
        member = interaction.guild.get_member(user_id)
        
        # Erstellung des Log-Channels
        log_channel_id = get_support_channel_log(interaction.guild_id)
        log_channel = interaction.client.get_channel(log_channel_id)

        await helper_cog.send_embed(log_channel,"TICKET CLOSED",
                            f"User: {member.mention} \n"
                            f"Datum: {datetime.datetime.now()} \n"
                            f"Typ: {typ.lower()} \n"
                            f"Ticket: {channel_name}",discord.Color.red(), member.avatar.url)
        
        await helper_cog.logMessage("support.py",
                                    f"Closed Ticket (Server-Name: {interaction.guild.name} | Ticket-Creator:{member} | Closer: {interaction.user})")
        # Wartet 3 Sekunden
        await asyncio.sleep(3)
        # Löscht den Channel
        await interaction.channel.delete()
        

class SupportCategories(discord.ui.Select):
    def __init__(self):
        # Setzt leeren Options-Array
        options = []

        # Geht durch jeden Support-Categorie Eintrag
        for key, data in SUPPORT_CATEGORIES_OPTIONS.items():
            # Fügt Optionen hinzu
            options.append(discord.SelectOption(label=data["label"], emoji=data["emoji"], value=key))
 
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

        # Rollen, die den Ticket-Channel sehen dürfen
        role_ids = get_support_roles(interaction.guild_id)
        
        await helper_cog.logMessage("support.py",f"Guild ID: {interaction.guild_id}")
        await helper_cog.logMessage("support.py",f"Role IDs: {repr(role_ids)}")
        
        # Setzt Leere Rolle 
        team_roles = []

        # Geht durch jede Rolle die in Support eingetragen ist 
        for role_id in role_ids:
            # Holt sich die Rolle
            role = guild.get_role(role_id)
            print(f"Role ID: {role_id} | Role: {role}")
            
            # Falls Rolle exsitiert
            if role is not None:
                team_roles.append(role)

        if not team_roles:
            await helper_cog.logError("support.py","roles wasn't found!")
            await interaction.response.send_message("Es ist ein Fehler beim erstellen des Tickets aufgetreten!", ephemeral=True)
            return
        
        # Holt sich den aktuellen Value
        selected_value = self.values[0]
        data = SUPPORT_CATEGORIES_OPTIONS[selected_value]
        
        # Hilfs Variable
        TICKET_NAME = f"ticket-{member.id}-{data['label']}"
        
        # Durchsucht alle Kategorien nach (name="")
        category = discord.utils.get(guild.categories, name="Tickets")
        
        # Falls Kategorie nicht gefunden wurde
        if category is None:
            await helper_cog.logError("support.py","Category wasn't found!")
            await interaction.response.send_message("Kategorie nicht gefunden!", ephemeral=True)
            return
        
        # Sucht nach einem Ticket (Verhindert Spam)
        ticket = discord.utils.get(guild.text_channels, name=TICKET_NAME.lower())
        if ticket is not None:
            await interaction.response.send_message(f"{member.mention} du hast bereits ein Ticket in dieser Kategorie erstellt: {ticket.mention}", ephemeral=True)
            return
        
        # Holt sich die ID des Support Log Channels
        log_channel_id = get_support_channel_log(interaction.guild_id)
        log_channel = interaction.client.get_channel(log_channel_id)
        
        if log_channel is None:
            await helper_cog.logError("support.py", f"Log Channel wurde nicht gefunden")
            await interaction.response.send_message("Es ist ein Fehler aufgetreten! (Kontaktiere einen Administrator)",ephemeral=True)
            return
        
        # Rechte für den Ticket-Channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True,send_messages=True)
        }

        # Alle Support-Rollen hinzufügen
        for role in team_roles:
            overwrites[role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True)

        # Ticket erstellen
        channel = await guild.create_text_channel(
            name=TICKET_NAME.lower(),
            category=category,
            overwrites=overwrites
        )
        
        

        await helper_cog.send_embed(log_channel,"TICKET CREATED",
                                               f"User: {member.mention} \n"
                                               f"Datum: {datetime.datetime.now()} \n"
                                               f"Typ: {data['label'].lower()}\n"
                                               f"Ticket: {channel.mention}",
                                               discord.Color.green(), member.avatar.url)
        

        # Antwort in dem Ticket-Channel
        await interaction.response.send_message(f"Ticket erstellt: {channel.mention}", ephemeral=True)        
        await helper_cog.logMessage("support.py",f"New Ticket (Server-Name: {interaction.guild.name} | User:{member.name})")

        # Sendet einen Ping an die Ticket-Rollen
        if team_roles:
            await channel.send(" ".join(role.mention for role in team_roles))

        description = SUPPORT_EMBED_MESSAGE.format(member=member.mention)

        # Erstellung von Embed Objekt & sendung
        await helper_cog.send_embed(channel, SUPPORT_EMBED_TITEL, description, discord.Color.green(), None)
        
        # Sendet Button
        await channel.send(view=TicketView())

class DropDown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.already_logged = False
        
    @commands.Cog.listener()
    async def on_ready(self):
        if self.already_logged:
            return
        self.already_logged = True

        helper_cog = self.bot.get_cog("Helper")
        
        if helper_cog is None:
            print("Fehler: Helper-Cog nicht gefunden!")
            return
        
        await helper_cog.logSuccess("support.py","Succcsessfully loaded")
   
        for guild in self.bot.guilds:
            #await helper_cog.logMessage("support.py", f"[DEBUG] Schleife erreicht: {guild.name} | {guild.id}")
            await helper_cog.logMessage("support.py", f"Server: {guild.name} | Guild-ID: {guild.id}")
            
            channel_id = get_support_channel_id(guild.id)
            if not channel_id:
                await helper_cog.logError("support.py",f"{guild.name}: No Support-Channel-ID was found")
            
            channel = self.bot.get_channel(channel_id)
            if not channel:
                await helper_cog.logError("support.py",f"{guild.name}: No Support-Channel was found")

            
            # Cleart bestimmte Anzahl an Messages
            await channel.purge(limit=10)
            await helper_cog.logMessage("support.py","Ticket was succcsessfully sent!")
            await helper_cog.send_embed(channel, SUPPORT_PREVIEW_EMBED_TITEL, SUPPORT_PREVIEW_EMBED_MESSAGE, discord.Color.blue(),None,SUPPORT_THUMBNAIL_URL)        
            await channel.send(view=SupportView())
        

async def setup(bot):
    await bot.add_cog(DropDown(bot))