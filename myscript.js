// Ensure the DOM is fully loaded before running
document.addEventListener("DOMContentLoaded", () => {
    // 1. Button click
    const btn = document.getElementById("myButton");
    if (btn) {
        btn.onclick = () => alert("Button clicked!");
    }

    // 2. Sidebar toggle
    const sidebarTrigger = document.querySelector("#btn-sidebar");
    const sidebarElement = document.querySelector(".sidebar");  
    if (sidebarTrigger && sidebarElement) {
        sidebarTrigger.addEventListener("click", () => {
            sidebarElement.classList.toggle("active");
        });
    }

    // 3. DataTable Init (only if table exists)
    const table = document.querySelector("#mytable");
    if (table) {
        // If you are using jQuery DataTables plugin
        $(table).DataTable();
        // Or if you are using vanilla DataTables:
        // new DataTable(table);
    }
});
