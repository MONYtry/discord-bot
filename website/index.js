const statsURL = "http://127.0.0.1:8000/stats";
const statusURL = "http://127.0.0.1:8000/status";
const guildsURL = "http://127.0.0.1:8000/guilds";
const commandsURL = "http://127.0.0.1:8000/commands";

async function getStatsData() {

    try {
        // Holt sich die URL
        const response = await fetch(statsURL);
        // Falls Fehler auftritt
        if (!response.ok) {
            throw new Error("Response Status: " + response.status);
        }
        // Mach aus der Antwort eine JSON-Formatierten Antwort
        const result = await response.json();

        // Setzt Werte in Anzeige
        const display_memberCount = document.getElementById("member-count");
        display_memberCount.textContent = "Nutzer: " + result.user_count;

        const display_guildCount = document.getElementById("guild-count");
        display_guildCount.textContent = "Server-Anzahl: " + result.guild_count;

        const display_cogCount = document.getElementById("module-count");
        display_cogCount.textContent = "Module: " + result.cog_count;
        
        const display_openTickets = document.getElementById("openTickets");
        display_openTickets.textContent = result.open_tickets;
        
        const display_totalclosedTickets = document.getElementById("closedTickets");
        display_totalclosedTickets.textContent = "Total closed Tickets: " + result.total_closed_tickets;

        const display_totalTickets = document.getElementById("totalTickets");
        display_totalTickets.textContent = "Total Tickets: " + result.total_tickets;

    }
    catch (error) {
        console.log(error);
    }
}

async function getStatusData() {
    try {
        // Holt sich die URL
        const response = await fetch(statusURL);
        // Falls Fehler auftritt
        if (!response.ok) {
            throw new Error("Response Status: " + response.status);
        }
        // Mach aus der Antwort eine JSON-Formatierten Antwort
        const result = await response.json();

        // Setzt Werte in Anzeige
        const display_online = document.getElementById("bot-online");
        display_online.textContent = "Bot-Online: " + result.bot_online;

        const display_username = document.getElementById("username");
        display_username.textContent = "Username: " + result.username;

        const display_ping = document.getElementById("ping");
        display_ping.textContent = "Ping: " + result.ping_ms;

        const display_uptime = document.getElementById("uptime");
        display_uptime.textContent = "Uptime: " + result.uptime;

        const display_cogCount = document.getElementById("ping");
        display_cogCount.textContent = "Ping: " + result.ping_ms;

        const display_api = document.getElementById("api_status");
        display_api.textContent = "API-STATUS: " + result.api_status;

    }
    catch (error) {
        console.log(error);
    }
}

async function getGuildsData() {
    try {
        // Holt sich die URL
        const response = await fetch(guildsURL);
        // Falls Fehler auftritt
        if (!response.ok) {
            throw new Error("Response Status: " + response.status);
        }
        // Mach aus der Antwort eine JSON-Formatierten Antwort
        const result = await response.json();

        // Setzt Werte in Anzeige
        const display_guilds = document.getElementById("guilds");
        display_guilds.textContent = "";

        for (var i = 0; i < result.guilds.length; i++)
        {
            display_guilds.textContent += result.guilds[i].name + ",";
        }

    }
    catch (error) {
        console.log(error);
    }
}



async function getCommandsData() {
    const container = document.getElementById("commands-container");
    
    if (!container)
    {
        console.error("commands dings wurde nicht gefunden");
    }

    try {
        // Holt sich die URL
        const response = await fetch(commandsURL);
        // Falls Fehler auftritt
        if (!response.ok) {
            throw new Error("Response Status: " + response.status);
        }
        // Mach aus der Antwort eine JSON-Formatierten Antwort
        const result = await response.json();
        
        // Erstellt Text falls Commands Vorhalten sind
        if (result.commands.length != 0)
        {
            const title = document.createElement("h2"); 
            title.className = "command-list-title";
            title.textContent = "Commands-List:"

            container.appendChild(title);
        }
        // Erstellt für jeden Command eine Info-Box
        for (var i = 0; i < result.commands.length; i++)
        {
            const div = document.createElement("div");
            const title = document.createElement("h2");
            const descripition = document.createElement("p");

            title.textContent = "/" + result.commands[i].name;
            descripition.textContent = result.commands[i].description;
            
            div.className = "command-box";
            title.className = "command-title";
            descripition.className = "command-description";

            div.appendChild(title);
            div.appendChild(descripition);
            container.appendChild(div);
        }
    }
    catch (error) {
        console.log(error);
    }
}


getGuildsData();
getStatsData();
getStatusData();
getCommandsData();