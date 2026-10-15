const statsURL = "http://127.0.0.1:8000/stats";
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


async function loadGuilds() {
    const display_loggingState = document.getElementById("loginState");
    display_loggingState.textContent = "❌ Not logged in";

    const response = await fetch("http://127.0.0.1:8000/api/guilds",
        {
            credentials: "include"
        }
    )

    if (response.status == 401)
    {
        console.log("Bitte melde dich zu erst mit Discord an!")
        return;
    }

    if (!response.ok)
    {
        console.log("Server konnte nicht gefunden werden");
        return;
    }
    
    const guilds = await response.json();
    

    const display_guilds = document.getElementById("guilds");
    display_guilds.textContent = "";

    display_loggingState.textContent = "✅ Logged in";

    for (var i = 0; i < guilds.length; i++) {
        display_guilds.textContent += guilds[i].name + ",";
    }
}

async function getAuthStatus(){
    const response = await fetch("http://127.0.0.1:8000/auth/status");
    const finalAntwort = await response.json();
    
}

loadGuilds();
getData();
  