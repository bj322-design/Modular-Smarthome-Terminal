export async function updateTasks() {
    const container = document.getElementById("google-tasks");
    if (!container) return;

    try {
        const response = await fetch('/api/google/tasks');
        const data = await response.json();

        // Display List Name and Tasks
        let html = `
            <div class="tasks-container">
                <div class="tasks-header">${data.list_name}</div>
                <ul class="tasks-list">
        `;

        data.tasks.forEach(task => {
            html += `<li class="task-item" data-id="${task.id}" style="cursor:pointer;">${task.title}</li>`;
        });

        html += `</ul></div>`;
        container.innerHTML = html;

        // Add Click Functionality
        document.querySelectorAll('.task-item').forEach(item => {
            item.addEventListener('click', async () => {
                const taskId = item.getAttribute('data-id');
                
                // Visual feedback: strike-through immediately
                item.style.textDecoration = "line-through";
                item.style.opacity = "0.5";

                await fetch('/api/google/tasks/complete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ task_id: taskId })
                });

                // Refresh the list after a short delay
                setTimeout(updateTasks, 1000);
            });
        });

    } catch (error) {
        console.error("Tasks sync failed:", error);
    }
}

setInterval(updateTasks, 60000);
updateTasks();