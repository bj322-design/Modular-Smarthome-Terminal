//TEMPERATURE
    async function updateTemp() {
        try {
            //temperature" to match flaskServer.py
            const response = await fetch("/temperature");
            const data = await response.json();

            // data.temp contains the formatted string from tempSensorWidget.update()
            document.getElementById("temp").innerText = data.temp;
        } catch (error) {
            console.error("Error updating temperature:", error);
        }
    }
    // Update Temperature every 2 seconds
    setInterval(updateTemp, 2000);
    updateTemp();