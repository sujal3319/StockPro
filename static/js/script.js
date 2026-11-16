
document.addEventListener("DOMContentLoaded", function () {

    // Product delete confirmation
    document.querySelectorAll(".delete-form").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            if (!confirm("Are you sure you want to delete this product?")) {
                event.preventDefault();
            }
        });
    });


    // Product search
    const searchInput = document.getElementById("productSearch");
    const productTable = document.getElementById("productTable");

    if (searchInput && productTable) {
        searchInput.addEventListener("input", function () {
            const value = this.value.toLowerCase();

            productTable.querySelectorAll("tbody tr").forEach(function (row) {
                row.style.display =
                    row.textContent.toLowerCase().includes(value) ? "" : "none";
            });
        });
    }


    // Bootstrap form validation
    document.querySelectorAll(".validate-form").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add("was-validated");
        });
    });


    // Automatically dismiss flash messages after 5 seconds
    document.querySelectorAll(".alert").forEach(function (alert) {
        setTimeout(function () {
            const instance = bootstrap.Alert.getOrCreateInstance(alert);
            instance.close();
        }, 5000);
    });


    // Active sidebar link
    const currentPath = window.location.pathname;

    document.querySelectorAll(".sidebar a[href]").forEach(function (link) {
        const linkPath = new URL(link.href).pathname;

        link.classList.toggle("active", linkPath === currentPath);
    });

});
