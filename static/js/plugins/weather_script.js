function getActiveClientId() {
    return localStorage.getItem('client_id') || 'default_client';
}

export async function updateCity() {
    const clientID = getActiveClientId();
    try {
        const response = await fetch(`/api/weather/smt??city=${city}clientID=${clientID}`)
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    } catch (error) {
        console.error("Weather City Change Failed:", error);
    }
}


export async function updateWeather() {
    const clientID = getActiveClientId();
    const addy = `/api/weather/smt?client_id=${clientID}`;
    try{
        const response = await fetch(addy);
        
        
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const data = await response.json();

        if (data.error) throw new Error(data.error);

        const weatherHTML = `
            <div class="weather-card">
                <div class="container">
                    <div class="city-name">${data.city}</div>
                    <div class="condition">${data.condition}</div>
                </div>
                <div class="current-temp">${data.current_temp}°</div>
                <div class="temp-range">
                    <span class="low">H: ${data.high}°</span>
                    <span class="high">L: ${data.low}°</span>
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

