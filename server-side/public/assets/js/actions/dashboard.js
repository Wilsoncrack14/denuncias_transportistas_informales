import ApiClient from './client.js';

import { paths, endpoints } from './variables.js'

class Dashboard extends ApiClient {
    constructor() {
        super();
        this.data = {
            total_users: 0,
            total_denuncias: 0,
            total_resueltas: 0,
            total_pendientes: 0,
            chart_data: []
        };
    }

    async init() {
        await this.getDashboardStats();
    }

    async getDashboardStats() {
        try {
            const { success, data } = await this.get(endpoints.reports);
            if (success) {
                this.data = data;
                console.log(data);
                this.renderChart();
            } else {
                this.error = 'Failed to load dashboard statistics.';
            }
        } catch (error) {
            console.error('Login failed:', error);
        }
    }

    renderChart() {
        const getTopSalesId = document.getElementById('total_denuncias_chart');
        if (getTopSalesId) {
            var options = {
                series: [
                    {
                        type: "line",
                        name: "Denuncias",
                        data: this.data.chart_data
                    }
                ],
                chart: {
                    height: 282,
                    type: "line",
                    animations: {
                        speed: 500
                    },
                    toolbar: {
                        show: false
                    }
                },
                colors: [
                    "#796df6"
                ],
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    curve: "smooth",
                    width: 3
                },
                xaxis: {
                    axisBorder: {
                        show: false,
                        color: '#e0e0e0'
                    },
                    axisTicks: {
                        show: true,
                        color: '#e0e0e0'
                    },
                    labels: {
                        style: {
                            colors: "#919aa3",
                            fontSize: "14px",
                            fontFamily: 'Outfit',
                        }
                    }
                },
                yaxis: {
                    tickAmount: 3,
                    labels: {
                        style: {
                            colors: "#919aa3",
                            fontSize: "14px",
                            fontFamily: 'Outfit',
                        }
                    }
                },
                legend: {
                    position: "top",
                    fontSize: "14px",
                    fontFamily: 'Outfit',
                    labels: {
                        colors: "#919aa3",
                    },
                    itemMargin: {
                        horizontal: 12,
                        vertical: 0
                    }
                },
                markers: {
                    size: 4,
                    colors: ["#796df6"],
                    strokeWidth: 2,
                    hover: {
                        sizeOffset: 2
                    }
                },
                grid: {
                    strokeDashArray: 5,
                    borderColor: "#e0e0e0"
                }
            };

            var chart = new ApexCharts(document.querySelector("#total_denuncias_chart"), options);
            chart.render();
        }
    }
}

document.addEventListener('alpine:init', () => {
    Alpine.data('dashboard', () => new Dashboard());
});