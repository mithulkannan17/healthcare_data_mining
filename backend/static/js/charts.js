const diseaseCtx = document.getElementById('diseaseChart');

if (diseaseCtx) {

    new Chart(diseaseCtx, {

        type: 'doughnut',

        data: {

            labels: Object.keys(diseaseData),

            datasets: [{

                label: 'Disease Distribution',

                data: Object.values(diseaseData),

                backgroundColor: [

                    '#38bdf8',
                    '#f43f5e',
                    '#22c55e',
                    '#eab308',
                    '#a855f7',
                    '#f97316',
                    '#14b8a6'

                ],

                borderWidth: 2,
                borderColor: '#0f172a'
            }]
        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    position: 'bottom',

                    labels: {
                        color: 'white',
                        padding: 20
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

                label: 'Patient Count',

                data: Object.values(severityData),

                backgroundColor: [

                    '#22c55e',
                    '#eab308',
                    '#ef4444'

                ],

                borderRadius: 10,
                borderSkipped: false
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
                    },

                    grid: {
                        color: '#1e293b'
                    }
                },

                y: {

                    beginAtZero: true,

                    ticks: {
                        color: 'white'
                    },

                    grid: {
                        color: '#1e293b'
                    }
                }
            }
        }
    });
}

const heatmapCtx = document.getElementById('regionHeatmap');

if (heatmapCtx) {

    const regions = Object.keys(regionDiseaseMap);

    const diseaseKeys = Object.keys(
        regionDiseaseMap[regions[0]]
    );

    const colorPalette = [

        '#38bdf8',
        '#ef4444',
        '#22c55e',
        '#eab308',
        '#a855f7',
        '#f97316',
        '#14b8a6'

    ];

    const datasets = diseaseKeys.map((disease, index) => ({

        label: disease,

        data: regions.map(

            region =>
                regionDiseaseMap[region][disease]
        ),

        backgroundColor:
            colorPalette[index % colorPalette.length],

        borderRadius: 6,
        borderSkipped: false
    }));

    new Chart(heatmapCtx, {

        type: 'bar',

        data: {

            labels: regions,

            datasets: datasets
        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    position: 'bottom',

                    labels: {
                        color: 'white',
                        padding: 15
                    }
                },

                title: {

                    display: true,

                    text: 'Regional Disease Distribution',

                    color: 'white',

                    font: {
                        size: 18
                    }
                }
            },

            scales: {

                x: {

                    stacked: true,

                    ticks: {
                        color: 'white'
                    },

                    grid: {
                        color: '#1e293b'
                    }
                },

                y: {

                    stacked: true,

                    beginAtZero: true,

                    ticks: {
                        color: 'white'
                    },

                    grid: {
                        color: '#1e293b'
                    }
                }
            }
        }
    });
}