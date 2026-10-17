const statsURL = "http://127.0.0.1:8000/stats";
const API = "http://127.0.0.1:8000";

async function getData(){
    try{
        const response = await fetch(statsURL);
        if (!response.ok)
        {
            console.log("Error");
        }
        const result = await response.json();

        const display_server = document.getElementById("used_by_servers");
        display_server.textContent = result.guild_count;

        const display_userCount = document.getElementById("used_by_users");
        display_userCount.textContent = result.user_count;
    }
    catch (error)
    {
        console.log("Error: " + error);
    }
}

async function loadProfile() {
    const response = await fetch(API + "/auth/me", {
        credentials: "include"
    });
    
    if (!response.ok)
    {
        console.log("Du bist nicht Angemeldet, bitte melde dich zuerst an!");
        return;
    }
    const user = await response.json();
    
    const name = document.createElement("p");
    name.textContent = "Name:" + user.global_name;

    const id = document.createElement("p");
    id.textContent = "Discord-ID:" + user.id;

    document.getElementById("profile").append(name, id);

    if (user.avatar) {
        const avatar = document.createElement("img");
        avatar.width = 80;
        avatar.alt = "Discord-Avatar";
        avatar.src = `https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}.png`;
        document.getElementById("profile").append(avatar);
    }
}

async function logout() {
    await fetch(API + "/auth/logout"), { method: "POST", credentials: "include" };
    console.log("Erfolgreich abgemeldet!");
}


loadProfile();
getData();
  