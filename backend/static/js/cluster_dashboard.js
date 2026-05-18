new Chart(

    document.getElementById('ageSeverityChart'),

    {

        type: 'bar',

        data: {

            labels: Object.keys(ageSeverity),

            datasets: [{

                label: 'Average Age',

                data: Object.values(ageSeverity),

                backgroundColor: '#38bdf8'
            }]
        },

        options: {

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
    }
);

const smokingLabels =
    Object.keys(smokingSeverity);

const severityKeys =
    Object.keys(
        smokingSeverity[smokingLabels[0]]
    );

const smokingDatasets =
    severityKeys.map((severity, index) => ({

        label: severity,

        data: smokingLabels.map(
            label => smokingSeverity[label][severity]
        ),

        backgroundColor: [
            '#38bdf8',
            '#ef4444',
            '#22c55e'
        ][index]
    }));

new Chart(

    document.getElementById('smokingChart'),

    {

        type: 'bar',

        data: {

            labels: smokingLabels,

            datasets: smokingDatasets
        },

        options: {

            plugins: {

                legend: {

                    labels: {
                        color: 'white'
                    }
                }
            },

            scales: {

                x: {

                    stacked: true,

                    ticks: {
                        color: 'white'
                    }
                },

                y: {

                    stacked: true,

                    ticks: {
                        color: 'white'
                    }
                }
            }
        }
    }
);

const alcoholLabels =
    Object.keys(alcoholSeverity);

const alcoholSeverityKeys =
    Object.keys(
        alcoholSeverity[alcoholLabels[0]]
    );

const alcoholDatasets =
    alcoholSeverityKeys.map((severity, index) => ({

        label: severity,

        data: alcoholLabels.map(
            label => alcoholSeverity[label][severity]
        ),

        backgroundColor: [
            '#eab308',
            '#ef4444',
            '#22c55e'
        ][index]
    }));

new Chart(

    document.getElementById('alcoholChart'),

    {

        type: 'bar',

        data: {

            labels: alcoholLabels,

            datasets: alcoholDatasets
        },

        options: {

            plugins: {

                legend: {

                    labels: {
                        color: 'white'
                    }
                }
            },

            scales: {

                x: {

                    stacked: true,

                    ticks: {
                        color: 'white'
                    }
                },

                y: {

                    stacked: true,

                    ticks: {
                        color: 'white'
                    }
                }
            }
        }
    }
);

const regions =
    Object.keys(regionDisease);

const diseaseKeys =
    Object.keys(
        regionDisease[regions[0]]
    );

const regionDatasets =
    diseaseKeys.map((disease, index) => ({

        label: disease,

        data: regions.map(
            region => regionDisease[region][disease]
        ),

        backgroundColor: [
            '#38bdf8',
            '#ef4444',
            '#22c55e',
            '#a855f7',
            '#eab308'
        ][index % 5]
    }));

new Chart(

    document.getElementById('regionChart'),

    {

        type: 'bar',

        data: {

            labels: regions,

            datasets: regionDatasets
        },

        options: {

            plugins: {

                legend: {

                    labels: {
                        color: 'white'
                    }
                }
            },

            scales: {

                x: {

                    stacked: true,

                    ticks: {
                        color: 'white'
                    }
                },

                y: {

                    stacked: true,

                    ticks: {
                        color: 'white'
                    }
                }
            }
        }
    }
);