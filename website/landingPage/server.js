const API = "http://127.0.0.1:8000";

// Holt sich die ID aus der URL 
const serverId = new URLSearchParams(window.location.search).get("id");

var useTickets = true;

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

        // Setzt die Werte
        document.getElementById("Input_Status_Channel_ID").value = antwort.statusInput;
        document.getElementById("Input_Welcome_Channel_ID").value = antwort.welcomeChannelInput;
        document.getElementById("Input_Join_Leave_Log_Channel_ID").value = antwort.join_leave_log_channel_id;
        document.getElementById("Input_Ticket_System_Display").textContent = ticket_status;
        document.getElementById("Input_Ban_Log_Channel_ID").value = antwort.ban_channel_id;
        document.getElementById("Input_Apply_Channel_ID").value = antwort.apply_channel_id;
        document.getElementById("Input_Ticket_System_Display").value = antwort.tickets_enabled;
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
    

    if ( 
        Input_Status_Channel_ID.value == "" || 
        Input_Welcome_Channel_ID.value == "" || 
        Input_Join_Leave_Log_Channel_ID.value == "" ||
        Input_Ban_Channel_ID.value == "") 
    {
        alert("Kein Bewerbungs-Channel gefunden!");
        return;
    }

    console.log("----- DEVELOPMENT-INFOMATION'S -----");
    console.log("Tickets-Status: " + useTickets);
    console.log("Status-Channel-ID: " + Input_Status_Channel_ID.value);
    console.log("Welcome-Channel-ID: " + Input_Welcome_Channel_ID.value);
    console.log("Join_leave_log-Channel-ID: " + Input_Join_Leave_Log_Channel_ID.value);
    console.log("ban_Channel_Id_Input: " + Input_Ban_Channel_ID.value);
    console.log("Bewerbungs ID: " + Input_Apply_Channel_ID.value)
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
                tickets_enabled: useTickets,
                Input_Status_Channel_ID: Input_Status_Channel_ID.value || null,
                Input_Welcome_Channel_ID: Input_Welcome_Channel_ID.value || null,
                Input_Join_Leave_Log_Channel_ID: Input_Join_Leave_Log_Channel_ID.value || null,
                Input_Ban_Channel_ID: Input_Ban_Channel_ID.value || null,
                Input_Apply_Channel_ID: Input_Apply_Channel_ID.value
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
