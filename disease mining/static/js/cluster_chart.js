const ctx = document.getElementById('clusterChart');

if (ctx) {

    const colors = [
        '#38bdf8',
        '#ef4444',
        '#22c55e',
        '#eab308',
        '#a855f7'
    ];

    const datasets = [];

    const uniqueClusters = [
        ...new Set(
            clusterData.map(
                item => item.cluster
            )
        )
    ];

    uniqueClusters.forEach(clusterId => {

        const points = clusterData
            .filter(
                item => item.cluster === clusterId
            )
            .map(
                item => ({
                    x: item.x,
                    y: item.y
                })
            );

        datasets.push({

            label: `Cluster ${clusterId}`,

            data: points,

            backgroundColor:
                colors[clusterId % colors.length],

            pointRadius: 6
        });
    });

    new Chart(ctx, {

        type: 'scatter',

        data: {
            datasets: datasets
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

                    title: {
                        display: true,
                        text: 'Principal Component 1',
                        color: 'white'
                    },

                    ticks: {
                        color: 'white'
                    }
                },

                y: {

                    title: {
                        display: true,
                        text: 'Principal Component 2',
                        color: 'white'
                    },

                    ticks: {
                        color: 'white'
                    }
                }
            }
        }
    });
}