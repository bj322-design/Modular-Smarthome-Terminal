export async function updateTimeZones() {
    const container = document.getElementById("time-zone");
    if (!container) return;

    try {
        const response = await fetch('/api/timezone/data');
        const data = await response.json();

        if (data.error) throw new Error(data.error);

        let html = `<div class="timezone-wrapper">`;
        data.forEach(loc => {
            html += `
                <div class="tz-entry">
                    <div class="tz-city">${loc.city}</div>
                    <div class="tz-time">${loc.time}</div>
                </div>
            `;
        });
        html += `</div>`;

        container.innerHTML = html;
    } catch (error) {
        console.error("TimeZone Update Failed:", error);
    }
}

setInterval(updateTimeZones, 10000); // Update every 10 seconds 
updateTimeZones();