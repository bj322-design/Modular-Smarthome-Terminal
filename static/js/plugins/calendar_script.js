let selectedDate = null;
let calendarInitialized = false;

function attachCalendarListeners() {
    const container = document.getElementById("calendar");

    if (!container) return;

    calendarInitialized = true; //  mark as initialized

    container.addEventListener("click", (e) => {
        const day = e.target.closest(".cal-day");
        if (!day) return;

        selectedDate = day.dataset.date;

        console.log("Calendar data:", window.calendarEvents);
        // SHOW TASKS FOR SELECTED DATE
        const eventsContainer = document.getElementById("selectedEventsContainer");
        const title = document.getElementById("eventsTitle");

        if (eventsContainer && title && window.calendarEvents) {
            let events = [];

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
                    div.innerHTML = `
                        <span>${e.title || e}</span>
                        <div style="margin-left:auto; display:flex; gap:6px;">
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

        // highlight
        document.querySelectorAll(".cal-day").forEach(d => d.style.outline = "none");
        day.style.outline = "2px solid #c084fc";

        // show input
        const taskSection = document.getElementById("taskSection");
        if (taskSection) taskSection.style.display = "block";

        // label
        const label = document.getElementById("selectedDateLabel");
        if (label) {
            label.innerText = "Editing tasks for: " + new Date(selectedDate).toDateString();
        }

        console.log("Selected date:", selectedDate);
    });
}

function addTask() {
    const input = document.getElementById("taskInput");
    const task = input.value;

    if (!selectedDate || !task) {
        alert("Select a date and enter a task");
        return;
    }

    fetch("/api/calendar/event", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            event: "add_event",
            args: {
                date: selectedDate,
                title: task
            }
        })
    })
    .then(() => {
        input.value = "";

        updateCalendar().then(() => {
            setTimeout(() => {
                const selected = document.querySelector(
                    `.cal-day[data-date="${selectedDate}"]`
                );

                if (selected) {
                    selected.click();

                    // optional safety re-click
                    setTimeout(() => {
                        selected.click();
                    }, 50);
                }
            }, 50);
        });
    });
}


function deleteTask(id, date) {
    fetch("/api/calendar/event", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
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
        headers: {
            "Content-Type": "application/json"
        },
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

//  ONLY ONE FUNCTION
export async function updateCalendar() {
    try {
        const response = await fetch('/widget/calendar');
        const html = await response.text();
        const container = document.getElementById('calendar');

        if (container) {
            container.innerHTML = html;

            //  IMPORTANT: re-read fresh data from HTML
            const scriptTag = container.querySelector("script");
            if (scriptTag) {
                eval(scriptTag.innerText); // updates window.calendarEvents
            }

            attachCalendarListeners();
        }
        setTimeout(() => {
            const today = document.querySelector(".cal-day.today");
            if (today) {
                today.click(); 
            }
        }, 50);

    } catch (error) {
        console.error('Calendar update failed:', error);
    }
}



updateCalendar().then(() => {
    setTimeout(() => {
        const today = document.querySelector(".cal-day.today");
        if (today) today.click();
    }, 50);
});

// update every 60s
setInterval(updateCalendar, 60000);

// make button work globally
window.addTask = addTask;
window.deleteTask = deleteTask;
window.editTask = editTask;