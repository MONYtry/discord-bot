
const API = "http://127.0.0.1:8000";

const serverId = new URLSearchParams(window.location.search).get("id");

let useTickets = true;


async function loadServer() {
    try {
        if (!serverId) {
            document.getElementById("serverName").textContent =
                "Keine Server-ID gefunden!";
            return;
        }

        const response = await fetch(API + "/auth/guilds", {
            credentials: "include"
        });

        if (!response.ok) {
            document.getElementById("serverName").textContent = "Bitte anmelden!";
            return;
        }

        const guilds = await response.json();

        let guild = null;

        for (let i = 0; i < guilds.length; i++) {
            if (guilds[i].id == serverId) {
                guild = guilds[i];
                break; 
            }
        }

        if (!guild) {
            document.getElementById("serverName").textContent = "Server nicht gefunden!";
            return;
        }

        document.getElementById("serverName").textContent = guild.name;

    } catch (error) {
        console.error("Fehler beim Laden des Servers:", error);
        document.getElementById("serverName").textContent =
            "Fehler beim Laden des Servers!";
    }
}

loadServer();


async function saveSettings() {

    const channelInput = document.getElementById("inputDing");
    const statusInput = document.getElementById("statusInput");
    const welcomeChannelInput = document.getElementById("welcomeChannelInput");
    const join_leave_log_channelInput = document.getElementById("join_leave_log_channel_input");
    const ban_Channel_Id_Input = document.getElementById("banChannelIdInput");

    if (!serverId) 
    {
        alert("Keine Server-ID gefunden!");
        return;
    }

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
