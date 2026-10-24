const API = "http://127.0.0.1:8000";

// Holt sich die ID aus der URL 
const serverId = new URLSearchParams(window.location.search).get("id");

async function getServer() {
    try {
        // Falls keine Server-ID gefunden wurde
        checkServerID();

        // Holt sich eine Antwort
        const response = await fetch(API + "/auth/guilds", {
            credentials: "include"
        });

        // Falls Fehler auftrit
        if (!response.ok) {
            document.getElementById("serverName").textContent = "Bitte anmelden!";
            return;
        }

        const guilds = await response.json();
        
        // Erstellt leeres Guild-Objekt
        let guild = null;

        // Geht durch alle Server
        for (let i = 0; i < guilds.length; i++) {
            // Falls der Server übereinstimmt
            if (guilds[i].id == serverId) {
                guild = guilds[i];
                break; 
            }
        }
        // Falls kein Server gefunden wurde
        if (!guild) {
            document.getElementById("serverName").textContent = "Server nicht gefunden!";
            return;
        }
        // Servr-Name setzen
        document.getElementById("serverName").textContent = guild.name;
        
        const serverAvatar = document.getElementById("serverAvatar");
        
        // Falls der Server ein Icon hat
        if (guild.icon) {
            serverAvatar.src = `https://cdn.discordapp.com/icons/${guild.id}/${guild.icon}.png?size=128`;
        }
        else {
            // Standard Icon
            serverAvatar.src = "https://cdn.discordapp.com/embed/avatars/0.png";
        }
        serverAvatar.style.display = "block";
        
        // Läd Settings
        getSettings();

    } 
    catch (error) 
    {
        console.error("Fehler beim Laden des Servers:", error);
        document.getElementById("serverName").textContent = "Fehler beim Laden des Servers!";
    }
}

async function checkServerID()
{
    if (!serverId) {
        alert("Keine Server-ID gefunden!");
        return;
    }
}

async function getSettings()
{
    try
    {    
        checkServerID();
     
        // Sendet Anfrage
        const response = await fetch(API + "/servers/" + serverId + "/settings",
            {
                // Methode = Get <= (Holen von Infomationen)
                method: "GET",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                }
            });

        // Antwort
        const antwort = await response.json();
        
        // Kleiner Dynamischer String zur Anzeige für Ticket_Status
        var ticket_status = "Stauts: ";
        if (antwort.tickets_enabled == "1")
            ticket_status += "[✅] - Aktiviert !"
        else
            ticket_status += "[💥] - Deaktiviert!"

        document.getElementById("Input_Ticket_System_Display").textContent = ticket_status;
        document.getElementById("Input_Ticket").value = antwort.tickets_enabled;
        document.getElementById("Input_Admin_Perm_Roles").value = (antwort.admin_perm_roles || []).join(",");

        // Setzt die Werte
        document.getElementById("Input_Status_Channel_ID").value = antwort.statusInput;
        document.getElementById("Input_Welcome_Channel_ID").value = antwort.welcomeChannelInput;
        document.getElementById("Input_Join_Leave_Log_Channel_ID").value = antwort.join_leave_log_channel_id;
        document.getElementById("Input_Ban_Log_Channel_ID").value = antwort.ban_channel_id;
        document.getElementById("Input_Apply_Channel_ID").value = antwort.apply_channel_id;
        document.getElementById("Input_Support_Channel_ID").value = antwort.support_channel_id;
        document.getElementById("Input_Ticket_Log_Channel_ID").value = antwort.support_log_channel_id;
        document.getElementById("Input_Timeout_Channel_ID").value = antwort.timeout_channel_id;
        document.getElementById("Input_Message_Log_Channel_ID").value = antwort.message_channel_id;
        document.getElementById("Input_Ticket_Log_Channel_ID").value = antwort.support_log_channel_id;
        document.getElementById("Input_Embed_Allowed_Roles_ID").value = (antwort.embed_allowed_roles || []).join(",");
        document.getElementById("Input_Support_Role").value = (antwort.support_roles || []).join(",");

    }
    catch (error)
    {
        console.log("Es ist ein Fehler aufgetreten!" , error)
    }
}


async function saveSettings() 
{
    // Nullpointer vermeiden
    checkServerID();

    // Holt sich die Eingabe-Felder
    const Input_Status_Channel_ID = document.getElementById("Input_Status_Channel_ID");
    const Input_Welcome_Channel_ID = document.getElementById("Input_Welcome_Channel_ID");
    const Input_Join_Leave_Log_Channel_ID = document.getElementById("Input_Join_Leave_Log_Channel_ID");
    const Input_Ban_Channel_ID = document.getElementById("Input_Ban_Log_Channel_ID");
    const Input_Apply_Channel_ID = document.getElementById("Input_Apply_Channel_ID");
    const Input_Support_Channel_ID = document.getElementById("Input_Support_Channel_ID");
    const Input_Support_Log_Channel_ID = document.getElementById("Input_Ticket_Log_Channel_ID");
    const Input_Timeout_Channel_ID = document.getElementById("Input_Timeout_Channel_ID");
    const Input_Message_Log_Channel_ID = document.getElementById("Input_Message_Log_Channel_ID");
    const Input_Embed_Allowed_Role = document.getElementById("Input_Embed_Allowed_Roles_ID");
    const Input_Support_Role = document.getElementById("Input_Support_Role");
    const Input_admin_roles = document.getElementById("Input_Admin_Perm_Roles");
    const use_tickets = document.getElementById("Input_Ticket");

    // Kleine Hilfe zum Debuggen etc.
    console.log("----- DEVELOPMENT-INFOMATION'S -----");
    console.log("Admin-Roles: " + Input_admin_roles.value);
    console.log("Tickets: " + use_tickets.value);
    console.log("Status-Channel-ID: " + Input_Status_Channel_ID.value);
    console.log("Welcome-Channel-ID: " + Input_Welcome_Channel_ID.value);
    console.log("Join_leave_log-Channel-ID: " + Input_Join_Leave_Log_Channel_ID.value);
    console.log("ban_Channel_Id_Input: " + Input_Ban_Channel_ID.value);
    console.log("Bewerbungs ID: " + Input_Apply_Channel_ID.value);
    console.log("Support ID: " + Input_Support_Channel_ID.value);
    console.log("Timeout ID: " + Input_Timeout_Channel_ID.value);
    console.log("MessageLoggingChannel: " + Input_Message_Log_Channel_ID.value);
    console.log("Input_Support_Log_Channel_ID: " + Input_Support_Log_Channel_ID.value);
    console.log("Input_Embed_Allowed_Role: " + Input_Embed_Allowed_Role.value);
    console.log("Input_Support_Role: " + Input_Support_Role.value);
    console.log("----- DEVELOPMENT-INFOMATION'S -----");
    
    const response = await fetch(
        API + "/servers/" + serverId + "/settings",
        {
            // Method POST = (Senden von Infomationen)
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },

            // Sendet angegebene Daten an das Backend 
            // Kleiner Reminder an mich selbst!!
            // Der erste Parameter muss mit dem Backend übereinstimmen!
            body: JSON.stringify({
                tickets_enabled: use_tickets.value,
                Input_Status_Channel_ID: Input_Status_Channel_ID.value || null,
                Input_Welcome_Channel_ID: Input_Welcome_Channel_ID.value || null,
                Input_Ban_Channel_ID: Input_Ban_Channel_ID.value || null,
                Input_Apply_Channel_ID: Input_Apply_Channel_ID.value || null,
                support_channel_id: Input_Support_Channel_ID.value || null,
                timeout_channel_id: Input_Timeout_Channel_ID.value || null,
                message_channel_id: Input_Message_Log_Channel_ID.value || null,
                support_log_channel_id: Input_Support_Log_Channel_ID.value || null,
                Input_Join_Leave_Log_Channel_ID: Input_Join_Leave_Log_Channel_ID.value || null,
                
                // map = Entfernt Leerzeichen am Anfang und Ende
                // Filter = Entfernt Leere Array Einträge
                embed_allowed_roles: Input_Embed_Allowed_Role.value.split(",").map(id => id.trim()).filter(id => id !== ""),
                support_roles: Input_Support_Role.value.split(",").map(id => id.trim()).filter(id => id !== ""),
                admin_perm_roles: Input_admin_roles.value.split(",").map(id => id.trim()).filter(id => id !== ""),
            })
        }
    );


    const result = await response.json();

    console.log("=== SERVER ANTWORT NACH DEM SPEICHERN ===");
    console.log(JSON.stringify(result, null, 2));

    if (response.ok) {
        alert("Einstellungen gespeichert!");
    } else {
        console.error("Speicherfehler:", result);
        alert("Speichern fehlgeschlagen: " + response.status);
    }

}

getServer();