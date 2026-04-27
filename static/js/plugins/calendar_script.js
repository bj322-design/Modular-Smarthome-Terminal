export async function updateCalendar() {
    try {
        const response = await fetch('/widget/calendar');
        const html = await response.text();
        const container = document.getElementById('calendar');
        if (container) container.innerHTML = html;
    } catch (error) {
        console.error('Calendar update failed:', error);
    }
}

// Update every 60 seconds
setInterval(updateCalendar, 60000);
// Run once immediately
updateCalendar(); 