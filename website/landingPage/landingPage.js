const stats = "/stats";
const apiBase = "http://127.0.0.1:8000";

async function getData() {
    try {
        const response = await fetch(apiBase + stats);
        if (!response.ok) {
            console.log("Error");
        }
        const result = await response.json();

        const display_server = document.getElementById("used_by_servers");
        display_server.textContent = result.guild_count;

        const display_userCount = document.getElementById("used_by_users");
        display_userCount.textContent = result.user_count;
    }
    catch (error) {
        console.log("Error:", error);
    }
}

getData();