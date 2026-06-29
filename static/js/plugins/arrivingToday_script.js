function getActiveClientId() {
    return localStorage.getItem('client_id') || 'default_client';
}

export async function updateArrivingToday() {
    const clientId = getActiveClientId();
    const container = document.getElementById("arrivingToday");
    if (!container) return;

    try {
        const response = await fetch(`/api/arriving-today/${clientId}`);
        const data = await response.json();

        if (data.count > 0) {
            let html = `<div class="pkg-count-header">📦 Arriving Today: ${data.count}</div>`;
            data.packages.forEach(pkg => {
                html += `
                    <div class="pkg-item today-priority">
                        <div class="pkg-name">${pkg.name}</div>
                        <div class="pkg-detail">${pkg.carrier} • ${pkg.status}</div>
                    </div>`;
            });
            container.innerHTML = html;
        } else {
            container.innerHTML = `<center><div class='no-packages'>No deliveries scheduled for today.
            <img src='static/images/package-icon.png' alt = 'No Packages' class = 'zero-packages'></center></div>`;
        }
    } catch (error) {
        console.error("Failed to update Arriving Today widget:", error);
    }
}

// Initial run and update every 5 minutes (300000ms)
updateArrivingToday();
setInterval(updateArrivingToday, 300000);