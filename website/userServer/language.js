
var isDE = true;

const translations = {
    DE: {
        title: "Server Dashboard",
        loading: "Server wird geladen...",
        back: "Zurück",
        settings: "⚙️ Bot-Einstellungen",
        maintenance: "Die Einstellungen befinden sich derzeit in Wartung und sind vorübergehend nicht verfügbar.",
        save: "💾 Einstellungen speichern",
        config: "⚙️ Bot-Konfiguration",
        configDescription: "Verwalte alle wichtigen Einstellungen deines Discord-Bots zentral und übersichtlich an einem Ort.",

        welcome: "👋 Welcome-Channel",
        welcomeDescription: "Lege fest, in welchem Channel neue Mitglieder automatisch begrüßt werden.",

        joinLeave: "📋 Join-/Leave-Logs",
        joinLeaveDescription: "Konfiguriere den Channel, in dem Beitritte und Austritte von Mitgliedern protokolliert werden.",

        ban: "🔨 Ban-Logs",
        banDescription: "Bestimme den Channel, in dem Sperrungen von Mitgliedern protokolliert werden.",

        teamRoles: "🔨 Team-Rollen",
        teamRolesDescription: "Lege fest, welche Rollen zu deinem Server-Team gehören.",

        teamList: "🔨 TEAM-LIST",
        teamListDescription: "Lege fest, in welchem Channel deine Team-Liste angezeigt wird.",

        status: "📡 Status-Channel",
        statusDescription: "Lege fest, in welchem Channel der Bot seinen aktuellen Status veröffentlicht.",

        application: "📝 Bewerbungs-Channel",
        applicationDescription: "Wähle den Channel, in dem Bewerbungen eingereicht und verwaltet werden.",

        timeout: "⏳ Timeout-Logs",
        timeoutDescription: "Lege fest, in welchem Channel Timeout-Aktionen dokumentiert werden.",

        messages: "💬 Nachrichten-Logs",
        messagesDescription: "Bestimme den Channel, in dem Nachrichtenereignisse protokolliert werden.",

        tickets: "🎫 Ticket-Logs",
        ticketsDescription: "Wähle den Channel, in dem Ticket-Erstellungen und weitere Ticket-Aktionen protokolliert werden.",

        embed: "🛡️ Embed-Berechtigungen",
        embedDescription: "Lege fest, welche Rollen die Berechtigung haben, die Embed-Funktionen zu nutzen.",

        supportRole: "🧑‍💻 Support-Rolle",
        supportRoleDescription: "Wähle die Rolle aus, die für die Bearbeitung von Support-Anfragen zuständig ist.",

        supportChannel: "🆘 Support-Channel",
        supportChannelDescription: "Lege fest, in welchem Channel Support-Anfragen entgegengenommen und bearbeitet werden.",

        admin: "⚙️ Admin-Berechtigungsrollen",
        adminDescription: "Bestimme, welche Rollen administrative Berechtigungen für den Bot erhalten.",

        joinRoles: "⚙️ Join-Rollen",
        joinRolesDescription: "Lege fest, welche Rollen Mitglieder automatisch beim Beitreten auf deinem Server erhalten.",

        trustedUrls: "✅ Vertrauenswürdige URLs",
        trustedUrlsDescription: "Verwalte vertrauenswürdige URLs, die von deinem Bot als sicher eingestuft werden.",

        ticketSystem: "🎟️ Ticket-System",
        ticketSystemDescription: "Aktiviere oder deaktiviere das Ticket-System deines Bots.",
        ticketStatus: "Aktueller Status: Unbekannt",

        statistics: "📊 Server-Statistik",
        statisticsDescription: "Verfolge die Entwicklung und wichtige Kennzahlen deines Discord-Servers übersichtlich in einer Statistik.",

        channelPlaceholder: "Channel-ID eingeben",
        rolePlaceholder: "Rollen-ID eingeben",
        rolesPlaceholder: "Rollen-IDs eingeben",
        joinRolesPlaceholder: "Rollen-IDs eingeben (mit Komma trennen)",
        urlsPlaceholder: "https://example.com, ...",
        ticketPlaceholder: "1 = Aktiviert, 0 = Deaktiviert"
    },

    EN: {
        title: "Server Dashboard",
        loading: "Loading server...",
        back: "Back",
        settings: "⚙️ Bot Settings",
        maintenance: "The settings are currently under maintenance and temporarily unavailable.",
        save: "💾 Save Settings",
        config: "⚙️ Bot Configuration",
        configDescription: "Manage all important settings of your Discord bot centrally and clearly in one place.",

        welcome: "👋 Welcome Channel",
        welcomeDescription: "Choose the channel where new members are automatically welcomed.",

        joinLeave: "📋 Join/Leave Logs",
        joinLeaveDescription: "Configure the channel where member joins and leaves are logged.",

        ban: "🔨 Ban Logs",
        banDescription: "Choose the channel where member bans are logged.",

        teamRoles: "🔨 Team Roles",
        teamRolesDescription: "Choose which roles belong to your server team.",

        teamList: "🔨 TEAM LIST",
        teamListDescription: "Choose the channel where your team list is displayed.",

        status: "📡 Status Channel",
        statusDescription: "Choose the channel where the bot publishes its current status.",

        application: "📝 Application Channel",
        applicationDescription: "Choose the channel where applications are submitted and managed.",

        timeout: "⏳ Timeout Logs",
        timeoutDescription: "Choose the channel where timeout actions are documented.",

        messages: "💬 Message Logs",
        messagesDescription: "Choose the channel where message events are logged.",

        tickets: "🎫 Ticket Logs",
        ticketsDescription: "Choose the channel where ticket creations and other ticket actions are logged.",

        embed: "🛡️ Embed Permissions",
        embedDescription: "Choose which roles are allowed to use the embed features.",

        supportRole: "🧑‍💻 Support Role",
        supportRoleDescription: "Select the role responsible for handling support requests.",

        supportChannel: "🆘 Support Channel",
        supportChannelDescription: "Choose the channel where support requests are received and handled.",

        admin: "⚙️ Admin Permission Roles",
        adminDescription: "Choose which roles receive administrative permissions for the bot.",

        joinRoles: "⚙️ Join Roles",
        joinRolesDescription: "Choose which roles members automatically receive when joining your server.",

        trustedUrls: "✅ Trusted URLs",
        trustedUrlsDescription: "Manage trusted URLs that are considered safe by your bot.",

        ticketSystem: "🎟️ Ticket System",
        ticketSystemDescription: "Enable or disable your bot's ticket system.",
        ticketStatus: "Current status: Unknown",

        statistics: "📊 Server Statistics",
        statisticsDescription: "Track the development and important metrics of your Discord server in a clear overview.",

        channelPlaceholder: "Enter Channel ID",
        rolePlaceholder: "Enter Role ID",
        rolesPlaceholder: "Enter Role IDs",
        joinRolesPlaceholder: "Enter Role IDs (separated by commas)",
        urlsPlaceholder: "https://example.com, ...",
        ticketPlaceholder: "1 = Enabled, 0 = Disabled"
    }
};

function changeLanguage() {
    isDE = !isDE;
    applyLanguage();
}

function applyLanguage() {

    const lang = isDE ? "DE" : "EN";

    // Website
    document.documentElement.lang = isDE ? "de" : "en";
    document.getElementById("serverTitle").textContent = translations[lang].title;

    // NICHT serverName überschreiben!
    // Dort steht später der echte Servername.

    // Buttons
    document.getElementById("backButton").textContent = translations[lang].back;
    document.getElementById("saveButton").textContent = translations[lang].save;
    document.getElementById("translateButton").textContent = lang;

    // Info Cards
    document.getElementById("settingsTitle").textContent = translations[lang].settings;
    document.getElementById("maintenanceDescription").textContent = translations[lang].maintenance;
    document.getElementById("configTitle").textContent = translations[lang].config;
    document.getElementById("configDescription").textContent = translations[lang].configDescription;

    // Welcome
    document.getElementById("welcomeTitle").textContent = translations[lang].welcome;
    document.getElementById("welcomeDescription").textContent = translations[lang].welcomeDescription;

    // Join / Leave
    document.getElementById("joinLeaveTitle").textContent = translations[lang].joinLeave;
    document.getElementById("joinLeaveDescription").textContent = translations[lang].joinLeaveDescription;

    // Ban
    document.getElementById("banTitle").textContent = translations[lang].ban;
    document.getElementById("banDescription").textContent = translations[lang].banDescription;

    // Team Roles
    document.getElementById("TeamRoles_Title").textContent = translations[lang].teamRoles;
    document.getElementById("TeamRoles_Description").textContent = translations[lang].teamRolesDescription;

    // Team List
    document.getElementById("teamListTitle").textContent = translations[lang].teamList;
    document.getElementById("teamListDescription").textContent = translations[lang].teamListDescription;

    // Status
    document.getElementById("statusTitle").textContent = translations[lang].status;
    document.getElementById("statusDescription").textContent = translations[lang].statusDescription;

    // Applications
    document.getElementById("applicationTitle").textContent = translations[lang].application;
    document.getElementById("applicationDescription").textContent = translations[lang].applicationDescription;

    // Timeout
    document.getElementById("timeoutTitle").textContent = translations[lang].timeout;
    document.getElementById("timeoutDescription").textContent = translations[lang].timeoutDescription;

    // Messages
    document.getElementById("messagesTitle").textContent = translations[lang].messages;
    document.getElementById("messagesDescription").textContent = translations[lang].messagesDescription;

    // Tickets
    document.getElementById("ticketsTitle").textContent = translations[lang].tickets;
    document.getElementById("ticketsDescription").textContent = translations[lang].ticketsDescription;

    // Embed
    document.getElementById("embedTitle").textContent = translations[lang].embed;
    document.getElementById("embedDescription").textContent = translations[lang].embedDescription;

    // Support
    document.getElementById("supportRoleTitle").textContent = translations[lang].supportRole;
    document.getElementById("supportRoleDescription").textContent = translations[lang].supportRoleDescription;

    document.getElementById("supportChannelTitle").textContent = translations[lang].supportChannel;
    document.getElementById("supportChannelDescription").textContent = translations[lang].supportChannelDescription;

    // Admin
    document.getElementById("adminTitle").textContent = translations[lang].admin;
    document.getElementById("adminDescription").textContent = translations[lang].adminDescription;

    // Join Roles
    document.getElementById("joinRolesTitle").textContent = translations[lang].joinRoles;
    document.getElementById("joinRolesDescription").textContent = translations[lang].joinRolesDescription;

    // Trusted URLs
    document.getElementById("trustedUrlsTitle").textContent = translations[lang].trustedUrls;
    document.getElementById("trustedUrlsDescription").textContent = translations[lang].trustedUrlsDescription;

    // Ticket System
    document.getElementById("ticketSystemTitle").textContent = translations[lang].ticketSystem;
    document.getElementById("ticketSystemDescription").textContent = translations[lang].ticketSystemDescription;
    document.getElementById("Input_Ticket_System_Display").textContent = translations[lang].ticketStatus;

    // Statistics
    document.getElementById("statisticsTitle").textContent = translations[lang].statistics;
    document.getElementById("statisticsDescription").textContent = translations[lang].statisticsDescription;

    // Placeholders
    document.getElementById("Input_Welcome_Channel_ID").placeholder = translations[lang].channelPlaceholder;
    document.getElementById("Input_Join_Leave_Log_Channel_ID").placeholder = translations[lang].channelPlaceholder;
    document.getElementById("Input_Ban_Log_Channel_ID").placeholder = translations[lang].channelPlaceholder;
    document.getElementById("Input_TeamRoles_List").placeholder = translations[lang].rolesPlaceholder;
    document.getElementById("Input_Teamlist_Channel_ID").placeholder = translations[lang].channelPlaceholder;
    document.getElementById("Input_Status_Channel_ID").placeholder = translations[lang].channelPlaceholder;
    document.getElementById("Input_Apply_Channel_ID").placeholder = translations[lang].channelPlaceholder;
    document.getElementById("Input_Timeout_Channel_ID").placeholder = translations[lang].channelPlaceholder;
    document.getElementById("Input_Message_Log_Channel_ID").placeholder = translations[lang].channelPlaceholder;
    document.getElementById("Input_Ticket_Log_Channel_ID").placeholder = translations[lang].channelPlaceholder;
    document.getElementById("Input_Embed_Allowed_Roles_ID").placeholder = translations[lang].rolesPlaceholder;
    document.getElementById("Input_Support_Role").placeholder = translations[lang].rolePlaceholder;
    document.getElementById("Input_Support_Channel_ID").placeholder = translations[lang].channelPlaceholder;
    document.getElementById("Input_Admin_Perm_Roles").placeholder = translations[lang].rolesPlaceholder;
    document.getElementById("Input_Join_Roles").placeholder = translations[lang].joinRolesPlaceholder;
    document.getElementById("Input_trusted_urls").placeholder = translations[lang].urlsPlaceholder;
    document.getElementById("Input_Ticket").placeholder = translations[lang].ticketPlaceholder;
}


applyLanguage();
