const stats = "/stats";
const auth = "/auth"
const apiBase = "http://127.0.0.1:8000";


async function loadProfile() {
    const response = await fetch(apiBase + auth + "/me", {
        credentials: "include"
    });
    
    if (!response.ok)
    {
        console.log("Du bist nicht Angemeldet, bitte melde dich zuerst an!");
        return;
    }

    const user = await response.json();
    loadGuilds();
    
    console.log(user);

    if (user.avatar) {
        const avatar = document.createElement("img");
        avatar.className = "avatar-img"
        avatar.width = 80;
        avatar.alt = "Discord-Avatar";
        avatar.src = `https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}.png`;
        document.getElementById("profile").append(avatar);
    }

    const name = document.createElement("p");
    name.textContent = "Name: " + user.username;

    const id = document.createElement("p");
    id.textContent = "Discord-ID: #" + user.id;

    document.getElementById("profile").append(name, id);
}


async function loadGuilds() {
    const response = await fetch(apiBase + auth + "/guilds", {
        credentials: "include"
    });

    if (!response.ok) {
        console.log("Du bist nicht angemeldet oder die Server konnten nicht geladen werden.");
        return;
    }

    const guilds = await response.json();
    const profile = document.getElementById("guildsElement");
    
    // Geht durch alle Server
    for (const guild of guilds) {

        const card = document.createElement("div");
        card.className = "server-card";

        const name = document.createElement("h3");
        name.textContent = guild.name;

        card.append(name);

        const guildId = guild.id;
        
        card.onclick = () => {
            window.location.href = `../userServer/server.html?id=${guildId}`;
        };
        profile.append(card);
    }
}

async function logout() {
    await fetch(apiBase + auth + "/logout", { method: "POST", credentials: "include" });
    
    console.log("Erfolgreich abgemeldet!");
    document.getElementById("profile").replaceChildren();
}

async function refreshProfile() {
    const profile = document.getElementById("profile");
    const guilds = document.getElementById("guildsElement");
    
    // Cleart den gesamten Inhalt
    guilds.replaceChildren();
    profile.replaceChildren();

    await loadProfile(); 
}

refreshProfile();