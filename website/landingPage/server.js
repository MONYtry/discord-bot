
const API = "http://127.0.0.1:8000";

// Holt sich die ID aus der URL 
const serverId = new URLSearchParams(window.location.search).get("id");

async function loadServer() {
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

    } catch (error) {
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
    try {
        
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
            ticket_status += "aktiviert!"
        else
            ticket_status += "deaktiviert!"

        // Setzt die Werte
        document.getElementById("statusInput").value = antwort.statusInput;
        document.getElementById("welcomeChannelInput").value = antwort.welcomeChannelInput;
        document.getElementById("join_leave_log_channel_input").value = antwort.join_leave_log_channel_id;
        document.getElementById("ticketSystemDisplay").textContent = ticket_status;
        document.getElementById("banChannelIdInput").value = antwort.ban_channel_id;
        document.getElementById("apply_channel_Input").value = antwort.apply_channel_id_Input;
    }
    catch (error)
    {
        console.log("Es ist ein Fehler aufgetreten!" , error)
    }
}


async function saveSettings() {

    const channelInput = document.getElementById("inputDing");
    const statusInput = document.getElementById("statusInput");
    const welcomeChannelInput = document.getElementById("welcomeChannelInput");
    const join_leave_log_channelInput = document.getElementById("join_leave_log_channel_input");
    const ban_Channel_Id_Input = document.getElementById("banChannelIdInput");

    checkServerID();

    if (channelInput.value == "" || 
        statusInput.value == "" || 
        welcomeChannelInput.value == "" || 
        join_leave_log_channelInput.value == "" ||
        ban_Channel_Id_Input.value == "") 
    {
        alert("Kein Bewerbungs-Channel gefunden!");
        return;
    }

    console.log("Tickets-Status: " + useTickets);
    console.log("Bewerbungs-ID: " + channelInput.value);
    console.log("Status-Channel-ID: " + statusInput.value);
    console.log("Welcome-Channel-ID: " + welcomeChannelInput.value);
    console.log("Join_leave_log-Channel-ID: " + join_leave_log_channelInput.value);
    console.log("ban_Channel_Id_Input: " + ban_Channel_Id_Input.value);
    
    const applyChannelId = channelInput.value.trim();
    
    const response = await fetch(
        API + "/servers/" + serverId + "/settings",
        {
            // Method POST = (Senden von Infomationen)
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                tickets_enabled: useTickets,
                apply_channel_id: applyChannelId || null,
                statusInput: statusInput.value || null,
                welcomeChannelInput: welcomeChannelInput.value || null,
                join_leave_log_channelInput: join_leave_log_channelInput.value || null,
                banChannelIdInput: ban_Channel_Id_Input.value || null
            })
        }
    );

    if (response.ok) 
    {
        alert("Einstellungen gespeichert!");
    }
    else 
    {
        const error = await response.text();
        console.error("Speicherfehler:", response.status, error);
        alert("Speichern fehlgeschlagen: " + response.status);
    }
}

loadServer();
