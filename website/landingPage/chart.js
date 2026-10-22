const ctx = document.getElementById("he");
const chartServerId = new URLSearchParams(window.location.search).get("id");
const statsURL = `http://127.0.0.1:8000/stats/${chartServerId}?minutes=5`;

let chart = null;

async function getMemberHistory() {
    try 
    {
        if (!chartServerId) throw new Error("Keine Server-ID in der URL gefunden!");

        const response = await fetch(statsURL, { credentials: "include" });
        if (!response.ok) throw new Error(`API-Fehler: ${response.status}`);

        const result = await response.json();
        return result.history || [];
    } 
    catch (error) 
    {
        console.error("Fehler beim Laden der Statistik:", error);
        return [];
    }
}

async function createDiagram() {
    const entries = await getMemberHistory();

    const labels = entries.map(entry =>
        entry.date.slice(11, 16)
    );

    const memberCounts = entries.map(entry =>
        entry.member_count
    );

    if (chart) {
        chart.data.labels = labels;
        chart.data.datasets[0].data = memberCounts;
        chart.update();
        return;
    }

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [{
                label: "Servermitglieder",
                data: memberCounts,
                borderColor: "#5865F2",
                backgroundColor: "#5865F233",
                fill: true,
                tension: 0.3
            }]
        }
    });
}


createDiagram();
setInterval(createDiagram, 60_000); // jede Minute aktualisieren