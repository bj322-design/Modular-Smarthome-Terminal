    export async function updateClock() {
        const response = await fetch("/time");
        const data = await response.json();

        document.getElementById("clock").innerText = data.time;
    }

 // update every 1 second
    setInterval(updateClock, 1000);

    // run once immediately
    updateClock();