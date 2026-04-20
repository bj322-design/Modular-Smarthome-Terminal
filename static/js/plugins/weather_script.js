export async function updateWeather() {
    try {
        const response = await fetch(`/api/weather/smt`);
        const data = await response.json();

        if (data.error) throw new Error(data.error);

        const weatherHTML = `
            <div class="weather-card">
                <div class="city-name">${data.city}</div>
                <div class="current-temp">${data.current_temp}°</div>
                <div class="condition">${data.condition}</div>
                <div class="temp-range">
                    <span class="low">H: ${data.low}°</span>
                    <span class="high">L: ${data.high}°</span>
                </div>
                <div class="weather-icon"><img src="${data.icon}" alt="weather icon"></div>
            </div>
        `;

        const container = document.getElementById("weather");
        if (container) {
            container.innerHTML = weatherHTML;
        }
    } catch (error) {
        console.error("Weather Update Failed:", error);
    }
}
    setInterval(updateWeather, 15000); //Update Every 15 seconds
    updateWeather();