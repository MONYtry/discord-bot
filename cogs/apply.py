from discord.ext import commands
import discord
import asyncio
import datetime
from config import (APPLY_CATEGORIES_OPTIONS,  
                    TICKET_PREWVIEW_EMBED_TITEL,
                    TICKET_PREVIEW_MESSAGE,
                    SUPPORT_THUMBNAIL_URL,
                    APPLY_QUESTIONS,APPLY_ALLOWED_ROLE_IDS,
                    TICKET_EMBED_DESCRIPTION)

from api.database import open_ticket,close_ticket, get_ticket_setting, get_apply_channel_id,get_support_channel_log


class SupportView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ApplyCategories())
        
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)    
        
    #  Erstellt Button
    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="ticket:close")
    async def close_ticket(self,interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Ticket wird in demnächst gelöscht!", ephemeral=True)
        
        # Holt sich den Namen des Tickets
        channel_name = interaction.channel.name

        helper_cog = interaction.client.get_cog("Helper")

        # Holt sich die UserID anhand des Ticket-Name
        # z.B ticket-123-bug -> ticket 123 bug -> user_id = 123
        user_id = int(channel_name.split("-")[1])
        typ = str(channel_name.split("-")[2])

        # Erstellt member Object anhand der UserID
        member = interaction.guild.get_member(user_id)
        if member:
            print(f"Ticket erstellt von: {member.name}")

        channel_id = get_support_channel_log(interaction.guild_id)
        log_channel = interaction.client.get_channel(channel_id)
        await helper_cog.send_embed(log_channel,"TICKET CLOSED",
                            f"User: {member.mention} \n"
                            f"Datum: {datetime.datetime.now()} \n"
                            f"Typ: {typ.lower()} \n"
                            f"Ticket: {channel_name}",discord.Color.red(), member.avatar.url)
        
        await helper_cog.logMessage("apply.py",
                                    f"Ticket was closed \n" 
                                    f"(Ticket creator:{member} | Close command sender: {interaction.user})")
        # Wartet 3 Sekunden
        await asyncio.sleep(3)
        close_ticket(interaction.channel.id,0)
        # Löscht den Channel
        await interaction.channel.delete()

class ApplyCategories(discord.ui.Select):
    def __init__(self):
        # Setzt Options
        options = [
            discord.SelectOption(label=data["label"], emoji=data["emoji"], value=key)
            # Geht durch alle SUPPORT_CATEGORIES_OPTIONS  
            for key, data in APPLY_CATEGORIES_OPTIONS.items()
        ]
        # Setzt applyDropDown Settings
        super().__init__(
            placeholder="Wähle ein Ticket aus!",
            options=options,
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):        
        # Holt sich den aktuellen Value
        selected_value = self.values[0]
        await interaction.response.send_modal(Formular(selected_value))
        

class applyDropDown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.already_logged = False
        self.clean_done = False
        
    @commands.Cog.listener()
    async def on_ready(self):
        helper_cog = self.bot.get_cog("Helper")

        if helper_cog is None:
            print("Fehler: Helper-Cog nicht gefunden!")
            return

        await helper_cog.logSuccess("apply.py", "Bewerbung bereit")

        for guild in self.bot.guilds:
            #await helper_cog.logMessage("apply.py", f"[DEBUG] Schleife erreicht: {guild.name} | {guild.id}")
            await helper_cog.logMessage("apply.py", f"Server: {guild.name} | Guild-ID: {guild.id}")
            
            channel_id = get_apply_channel_id(guild.id)
            if not channel_id:
                await helper_cog.logError("apply.py", f"{guild.name}: No Apply-Channel-ID was found!")

            channel = self.bot.get_channel(channel_id)
            if not channel:
                await helper_cog.logError("apply.py", f"{guild.name}: No Apply-Channel was found!")
                return
            
            await helper_cog.logMessage("apply.py", f"{guild.name}: {channel}")
            
            embed = discord.Embed(
                title=TICKET_PREWVIEW_EMBED_TITEL,
                description=TICKET_PREVIEW_MESSAGE,
                color=discord.Color.blue())
            
            embed.set_thumbnail(url=SUPPORT_THUMBNAIL_URL)
            
            # Löscht 10 Messages von dem Channel
            if self.clean_done is False:
                await channel.purge(limit=10)
                self.clean_done = True
            
            try:
                await channel.send(embed=embed, view=SupportView())
                #await helper_cog.logMessage("apply.py",f"Apply-Embed gesendt: {guild.name}")
            except discord.HTTPException as e:
                await helper_cog.logMessage("apply.py",f"Embed konnte nicht gesendet werden: {e}")


# Erstellt eine Class mit Discord UI & Titel
class Formular(discord.ui.Modal, title="Bewerbung"):

    def __init__(self, selected_value):
        super().__init__()
        self.selected_value = selected_value
        
        for label, placeholder in APPLY_QUESTIONS[selected_value]:
            self.add_item(discord.ui.TextInput(
                label=label,
                placeholder=placeholder,
                style=discord.TextStyle.paragraph,
                max_length=500,
                required=True))
    
    # Sobald abgeschickt wird
    async def on_submit(self, interaction: discord.Interaction):

        if not get_ticket_setting(interaction.guild.id):
            await interaction.response.send_message("Das Ticket-System ist aktuell deaktiviert!", ephemeral=True)
            return
            
        # Holt sich den aktuellen Value
        selected_value = self.selected_value
        data = APPLY_CATEGORIES_OPTIONS[selected_value]

        description = TICKET_EMBED_DESCRIPTION.format(member=interaction.user.mention)
        
        # Embed wird erstellt
        introEmbed = discord.Embed(
            # Setzt den eben erstellten Titel
            title="Info-Bewerbung",
            description = description,
            color=discord.Color.blue()
        )

        introEmbed.set_footer(text = "Developer Academy Bot • Made with Love ❤️")

        embed = discord.Embed(
            title=f"📨 Neue {data['label']}-Bewerbung",
            description=(
                f"Eine neue Bewerbung von {interaction.user.mention} "
                "ist eingegangen.\n"
                "━━━━━━━━━━━━━━━━━━━━"
            ),
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )

        # Geht durch alle Children
        for item in self.children:
            # Wenn es ein discord.UI ist 
            if isinstance(item,discord.ui.TextInput):
                # Fügt Embed add_Field hinzu 
                embed.add_field(name=item.label, value=item.value or "Keine Antwort", inline=False)
        
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_footer(text="Developer Academy • Bewerbungsmanagement",
                         icon_url=interaction.client.user.display_avatar.url)
        
        # Hilfs-Variablen
        guild = interaction.guild
        member = interaction.user
        helper_cog = interaction.client.get_cog("Helper")

        # Rollen, die den Ticket-Channel sehen dürfen
        # Geht durch alle Rollen in dem Discord-Server, falls Rollen.id passt <- Hinzufügen
        team_roles = [
            role for role in guild.roles
                if role.id in APPLY_ALLOWED_ROLE_IDS]
        
        if team_roles is None:
            await helper_cog.logError("apply.py","roles wasn't found!")
            await interaction.response.send_message("Es ist ein Fehler beim erstellen des Tickets aufgetreten!")
            return
        
        # Hilfs Variable
        TICKET_NAME = f"ticket-{member.id}-{data['label']}"
        
        # Durchsucht alle Kategorien nach (name="")
        category = discord.utils.get(guild.categories, name="Tickets")
        
        # Falls Kategorie nicht gefunden wurde
        if category is None:
            await helper_cog.logError("apply.py","Category wasn't found!")
            await interaction.response.send_message("Kategorie nicht gefunden!", ephemeral=True)
            return
        
        # Sucht nach einem Ticket (Verhindert Spam)
        ticket = discord.utils.get(guild.text_channels, name=TICKET_NAME.lower())
        if ticket is not None:
            await interaction.response.send_message(f"{member.mention} du hast bereits ein Ticket in dieser Kategorie erstellt: {ticket.mention}", ephemeral=True)
            return
        
        # Erstellt Rechte
        overwrites = {
                        # Überschreibt die Rechte des @Everyones (Niemand sieht diesen Channel)
                        guild.default_role: discord.PermissionOverwrite(view_channel=False),
                        # Nun sieht member diesen Channel
                        member: discord.PermissionOverwrite(view_channel=True,send_messages=True),
                    }
        
        # Überschreibt Rechte für Team-Rollen
        for role in team_roles:
            overwrites[role] = discord.PermissionOverwrite(view_channel=True,send_messages=True)

        # Erstellt einen Text-Channel
        channel = await guild.create_text_channel(
            # Setzt den Namen des Channels
            name = TICKET_NAME,
            # Setzt die Category
            category = category,
            overwrites=overwrites)
        
        # Datenbank 
        open_ticket(channel.id,1,guild.id)

        channel_id = get_support_channel_log(interaction.guild_id)
        log_channel = interaction.client.get_channel(channel_id)
        await helper_cog.send_embed(log_channel,"TICKET CREATED",
                                               f"User: {member.mention} \n"
                                               f"Datum: {datetime.datetime.now()} \n"
                                               f"Typ: {data['label'].lower()}\n"
                                               f"Ticket: {channel.mention}",
                                               discord.Color.green(), member.avatar.url)

        # Antwort in dem Ticket-Channel
        await interaction.response.send_message(f"Ticket erstellt: {channel.mention}", ephemeral=True)        
        await helper_cog.logMessage("apply.py",f"Ticket was created (User:{member.name})")

        # Sendet einen Ping an die angegebene Rolle
        # .join hilft um ein einer Zeile zu bleiben
        await channel.send("".join(role.mention for role in team_roles))

        await channel.send(embed=introEmbed)
        await channel.send(embed=embed)
        
        # Sendet Button
        await channel.send(view=TicketView())    

async def setup(bot):
    await bot.add_cog(applyDropDown(bot))
    bot.add_view(TicketView())