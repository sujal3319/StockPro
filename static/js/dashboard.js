
document.addEventListener("DOMContentLoaded", function () {

    const container = document.getElementById("stockChartContainer");

    if (!container) return;

    if (typeof Chart === "undefined") {
        console.error("Chart.js is not loaded.");
        return;
    }

    let labels;
    let quantities;

    try {
        labels = JSON.parse(container.dataset.labels || "[]");
        quantities = JSON.parse(container.dataset.quantities || "[]");
    } catch (error) {
        console.error("Invalid chart data:", error);
        return;
    }

    const canvas = document.getElementById("stockChart");

    if (!canvas) return;

    if (labels.length === 0) {
        canvas.replaceWith(
            Object.assign(document.createElement("p"), {
                textContent: "No inventory data available.",
                className: "text-center text-muted"
            })
        );
        return;
    }

    new Chart(canvas, {
        type: "doughnut",

        data: {
            labels: labels,
            datasets: [{
                label: "Stock Quantity",
                data: quantities,
                borderWidth: 2,
                hoverOffset: 8
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                legend: {
                    position: "bottom"
                },

                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return context.label + ": " +
                                context.raw + " units";
                        }
                    }
                }
            }
        }
    });

});
