export async function updateLight() {
    const container = document.getElementById("fake-light");
    if (!container) return;

    try {
        const response = await fetch('/api/light/status');
        const data = await response.json();

        // Determine which icon to use based on the state
        const iconSrc = data.state === 'ON' ?  './static/images/LightOn.png' : './static/images/LightOff.png';

        container.innerHTML = `
            <div class="light-card ${data.state.toLowerCase()}">
                <div class="light-label">Living Room Light</div>
                <div class="light-status">${data.state}</div>
                <div class="light-icon">
                    <img src="${iconSrc}" alt="light-icon">
                </div>
                <button id="toggle-btn" class="switch-btn">
                    ${data.state === 'OFF' ? 'Turn On' : 'Turn Off'}
                </button>
            </div>
        `;

        document.getElementById("toggle-btn").onclick = async () => {
            // Disable the button briefly to prevent double-clicks
            document.getElementById("toggle-btn").disabled = true;
            await fetch('/api/light/toggle', { method: 'POST' });
            updateLight(); 
        };
    } catch (error) {
        console.error("Light Switch sync failed:", error);
    }
}



// Initial calls
setInterval(updateLight, 1000);
updateLight();