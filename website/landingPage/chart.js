const ctx = document.getElementById("he");
const chartServerId = new URLSearchParams(window.location.search).get("id");
const statsURL = `http://127.0.0.1:8000/stats/${chartServerId}?minutes=5`;

let chart = null;

async function getMemberHistory() {
    try 
    {
        if (!chartServerId) throw new Error("Keine Server-ID in der URL gefunden!");

        const response = await fetch(statsURL, {
             credentials: "include" 
        });

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

async function createDiagram() 
{
    
    const entries = await getMemberHistory();
    const labels = [];
    if (entries == null)
    {
        console.log("Es wurden keine Einträge gefunden");
        if (!chart)
            return;

        chart.data.datasets[0].data = 0;
        chart.update();
        return;
    }

    // Geht durch alle Einträge
    for (var i = 0; i < entries.length; i++)
    {
        // Fügt die Uhrzeit ein
        labels.push(entries[i].date.slice(11,16));
    }

    // Erstellt leeres Objekt
    const memberCounts = [];
    
    // Geht durch alle Einträge
    for (var i = 0; i < entries.length; i++)
    {
        // Setzt Member-Anzahl
        memberCounts.push(entries[i].member_count); 
    }

    // Falls Chart bereits exisitiert, nur updaten
    if (chart) {
        chart.data.labels = labels;
        chart.data.datasets[0].data = memberCounts;
        chart.update();
        return;
    }
    // Erstellung des Charts mit Chart.js :)
    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Servermitglieder",
                data: memberCounts,
                borderColor: "#5865F2",
                backgroundColor: "#5865F233",
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            scales: {
                y: {
                    ticks: {
                        precision: 0,
                        stepSize: 1
                    }
                }
            }
        }
    });
}


createDiagram();
setInterval(createDiagram, 120_000); // jede 2te Minute aktualisieren