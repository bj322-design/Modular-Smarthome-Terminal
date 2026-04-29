document.addEventListener("DOMContentLoaded", () => {
    loadLayout();
});

async function loadLayout() {
    const res = await fetch("/api/layout");
    const data = await res.json();

    const widgets = data.widgets;

    // Fill all dropdowns
    for (let i = 1; i <= 9; i++) {
        const select = document.getElementById("box" + i);

        // clear existing
        select.innerHTML = "";

        widgets.forEach(w => {
            const option = document.createElement("option");
            option.value = w.id;
            option.textContent = w.name;
            select.appendChild(option);
        });
    }

    // Set current layout
    widgets.forEach(w => {
        const position = (w.row - 1) * 3 + w.col; // converts row/col → box #
        const select = document.getElementById("box" + position);

        if (select) {
            select.value = w.id;
        }
    });
}