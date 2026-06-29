console.log("date script loaded");

async function updateDate() {
    const widget = document.getElementById('widget-Date');
    console.log("date widget found:", widget);

    if (!widget) return;

    try {
        await fetch('/api/date');

        const d = new Date();
        
        const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        const dayName = days[new Date().getDay()]; 

        const month = d.toLocaleString('en-US', { month: 'long' });
        const day = d.getDate();
        const year = d.getFullYear();

        widget.innerHTML = `
            <div class="date-container">
                <div class="date-name">${dayName}</div>
                <div class="date-month">${month} ${day}</div>
                <div class="date-year">${year}</div>
            </div>
        `;
    } catch (err) {
        console.error("Date widget error:", err);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    updateDate();
    setInterval(updateDate, 60000);
});