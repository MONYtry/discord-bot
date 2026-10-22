
const ctx = document.getElementById("he");

const chartServerId = new URLSearchParams(window.location.search).get("id");

const statsURL = `http://127.0.0.1:8000/stats/${chartServerId}?minutes=60`;

async function getMemberHistory() {
    try {
        if (!chartServerId) {
            throw new Error("Keine Server-ID in der URL gefunden!");
        }

        const response = await fetch(statsURL, {
            credentials: "include"
        });

        if (!response.ok) {
            throw new Error(`API-Fehler: ${response.status}`);
        }

        const result = await response.json();
        return result.history || [];

    } catch (error) {
        console.error("Fehler beim Laden der Statistik:", error);
        return [];
    }
}

async function createDiagram() {
    if (!ctx) {
        console.error("Canvas mit ID 'he' nicht gefunden!");
        return;
    }

    const history = await getMemberHistory();

    const labels = history.map(entry => {
        const date = new Date(entry.date);
        return date.toLocaleTimeString("de-DE", {
            hour: "2-digit",
            minute: "2-digit"
        });
    });

    const memberCounts = history.map(
        entry => entry.member_count
    );

    new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [{
                label: "Servermitglieder",
                data: memberCounts,
                borderColor: "#5865F2",
                backgroundColor: "#5865F233",
                borderWidth: 2,
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Uhrzeit"
                    }
                },
                y: {
                    beginAtZero: false,
                    ticks: {
                        precision: 0
                    },
                    title: {
                        display: true,
                        text: "Mitglieder"
                    }
                }
            }
        }
    });
}

createDiagram();
