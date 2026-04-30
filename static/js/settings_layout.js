document.addEventListener("DOMContentLoaded", () => {
    loadLayout();

    const resetButton = document.getElementById("reset-layout-btn");

    if (resetButton) {
        resetButton.addEventListener("click", resetLayout);
    }
});


document.addEventListener("DOMContentLoaded", () => {

    const SubmitBut = document.getElementById("save-layout-btn");

    if(SubmitBut)
        SubmitBut.addEventListener("click", submit);
})

async function loadLayout() {
    const res = await fetch("/api/layout");
    const data = await res.json();

    const widgets = data.widgets;

    for (let i = 1; i <= 9; i++) {
        const select = document.getElementById("box" + i);
        if (!select) continue;

        select.innerHTML = "";

        widgets.forEach(w => {
            const option = document.createElement("option");
            option.value = w.id;
            option.textContent = w.name;
            select.appendChild(option);
        });
    }

    widgets.forEach(w => {
        const boxNumber = (w.row - 1) * 3 + w.col;
        const select = document.getElementById("box" + boxNumber);

        if (select) {
            select.value = w.id;
        }
    });
}

async function resetLayout() {
    await fetch("/api/layout/default", {
        method: "POST"
    });

    await loadLayout();
}

async function submit() {
    const updatedWidgets = [];

    // Loop through the 9 boxes to get current selections
    for (let i = 1; i <= 9; i++) {
        const select = document.getElementById("box" + i);
        if (select) {
            const row = Math.ceil(i / 3);
            const col = (i - 1) % 3 + 1;
            
            updatedWidgets.push({
                id: select.value,
                name: select.options[select.selectedIndex].text,
                row: row,
                col: col
            });
        }
    }

    // Send the collected data to the API
    await fetch("/api/layout", {
        method: "POST", // Capitalized for best practice
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ widgets: updatedWidgets })
    });

    await loadLayout();
}