const diseaseCtx = document.getElementById('diseaseChart');

if (diseaseCtx) {

    new Chart(diseaseCtx, {
        type: 'pie',

        data: {
            labels: Object.keys(diseaseData),

            datasets: [{
                data: Object.values(diseaseData),

                backgroundColor: [
                    '#38bdf8',
                    '#f43f5e',
                    '#22c55e',
                    '#eab308',
                    '#a855f7',
                    '#f97316',
                    '#14b8a6'
                ]
            }]
        },

        options: {
            responsive: true,

            plugins: {
                legend: {
                    labels: {
                        color: 'white'
                    }
                }
            }
        }
    });
}

const severityCtx = document.getElementById('severityChart');

if (severityCtx) {

    new Chart(severityCtx, {

        type: 'bar',

        data: {
            labels: Object.keys(severityData),

            datasets: [{
                label: 'Cases',
                data: Object.values(severityData),

                backgroundColor: [
                    '#22c55e',
                    '#eab308',
                    '#ef4444'
                ]
            }]
        },

        options: {
            responsive: true,

            plugins: {
                legend: {
                    labels: {
                        color: 'white'
                    }
                }
            },

            scales: {
                x: {
                    ticks: {
                        color: 'white'
                    }
                },

                y: {
                    ticks: {
                        color: 'white'
                    }
                }
            }
        }
    });
}