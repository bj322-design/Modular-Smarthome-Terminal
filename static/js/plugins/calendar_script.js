/**
 * PREREQUISITES FOR THIS FILE:
 * 1. An HTML container with id="calendar".
 * 2. An API endpoint at /widget/calendar that returns HTML.
 * 3. An API endpoint at /api/calendar/event that handles POST requests.
 * 4. A global window.calendarEvents array (usually provided by the server-side HTML).
 */

let selectedDate = null;
let calendarInitialized = false;

/**
 * Attaches event listeners to the calendar container.
 * Uses delegation so we don't have to re-bind listeners to every single day.
 */
function attachCalendarListeners() {
    const container = document.getElementById("calendar");
    if (!container) return;

    calendarInitialized = true;

    container.addEventListener("click", (e) => {
        const day = e.target.closest(".cal-day");
        if (!day) return;

        selectedDate = day.dataset.date;

        // UI Elements
        const eventsContainer = document.getElementById("selectedEventsContainer");
        const title = document.getElementById("eventsTitle");
        const taskSection = document.getElementById("taskSection");
        const label = document.getElementById("selectedDateLabel");

        if (eventsContainer && title && window.calendarEvents) {
            let events = [];

            // Find events for the clicked date from the global data store
            window.calendarEvents.forEach(week => {
                week.forEach(dayData => {
                    if (dayData.date_str === selectedDate) {
                        events = dayData.events;
                    }
                });
            });

            title.innerText = new Date(selectedDate).toDateString();
            eventsContainer.innerHTML = "";

            if (events.length > 0) {
                events.forEach(e => {
                    const div = document.createElement("div");
                    div.className = "cal-event-item";
                    div.style.display = "flex";
                    div.style.marginBottom = "5px";
                    div.innerHTML = `
                        <span>${e.title || e}</span>
                        <div style="margin-left:auto; display:flex; gap:6px;">
                        <div class="cal-header">
                            <button onclick="editTask(${e.id || 0}, '${selectedDate}', '${e.title || e}')">✎</button>
                            <button onclick="deleteTask(${e.id || 0}, '${selectedDate}')">✕</button>
                        </div>
                    `;
                    eventsContainer.appendChild(div);
                });
            } else {
                eventsContainer.innerHTML = `<div class="cal-no-events">No tasks</div>`;
            }
        }

        // Visual Highlight: Clear others, highlight selected
        document.querySelectorAll(".cal-day").forEach(d => d.style.outline = "none");
        day.style.outline = "2px solid #c084fc";

        // Toggle task input visibility
        if (taskSection) taskSection.style.display = "block";
        if (label) {
            label.innerText = "Editing tasks for: " + new Date(selectedDate).toDateString();
        }

        console.log("Selected date:", selectedDate);
    });
}

/**
 * Sends a new task to the server and refreshes the UI.
 */
function addTask() {
    const input = document.getElementById("taskInput");
    const task = input.value;

    if (!selectedDate || !task) {
        alert("Select a date and enter a task");
        return;
    }

    fetch("/api/calendar/event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            event: "add_event",
            args: { date: selectedDate, title: task }
        })
    })
    .then(() => {
        input.value = "";
        updateCalendar().then(() => {
            // File 1 logic: Re-click the date so the new task appears immediately
            setTimeout(() => {
                const selected = document.querySelector(`.cal-day[data-date="${selectedDate}"]`);
                if (selected) {
                    selected.click();
                    setTimeout(() => selected.click(), 50); // Safety re-click
                }
            }, 50);
        });
    });
}

function deleteTask(id, date) {
    fetch("/api/calendar/event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            event: "delete_event",
            args: { id, date }
        })
    }).then(() => {
        updateCalendar().then(() => {
            setTimeout(() => {
                const day = document.querySelector(`[data-date="${date}"]`);
                if (day) day.click();
            }, 50);
        });
    });
}

function editTask(id, date, oldTitle) {
    const newTitle = prompt("Edit task:", oldTitle);
    if (!newTitle) return;

    fetch("/api/calendar/event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            event: "edit_event",
            args: { id, date, title: newTitle }
        })
    }).then(() => {
        updateCalendar().then(() => {
            setTimeout(() => {
                const day = document.querySelector(`[data-date="${date}"]`);
                if (day) day.click();
            }, 50);
        });
    });
}

/**
 * Fetches the latest calendar HTML from the server and injects it.
 */
export async function updateCalendar() {
    try {
        const response = await fetch('/widget/calendar');
        const html = await response.text();
        const container = document.getElementById('calendar');

        if (container) {
            container.innerHTML = html;

            // Execute the script embedded in the fetched HTML to update window.calendarEvents
            const scriptTag = container.querySelector("script");
            if (scriptTag) {
                eval(scriptTag.innerText); 
            }

            attachCalendarListeners();
        }

        // File 1 logic: Default back to "Today" after background updates
        setTimeout(() => {
            const today = document.querySelector(".cal-day.today");
            if (today) today.click(); 
        }, 50);

    } catch (error) {
        console.error('Calendar update failed:', error);
    }
}

function changeMonth(direction) {
    fetch("/api/calendar/event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            event: direction === "next" ? "next_month" : "prev_month"
        })
    })
    .then(res => res.json())
    .then(() => updateCalendar())
    .catch(err => console.error("ERROR:", err));
}

window.changeMonth = changeMonth;


// Initialize on Load
updateCalendar().then(() => {
    setTimeout(() => {
        const today = document.querySelector(".cal-day.today");
        if (today) today.click();
    }, 50);
});

// Background Sync
setInterval(updateCalendar, 60000);

// make button work globally
window.addTask = addTask;
window.deleteTask = deleteTask;
window.editTask = editTask;