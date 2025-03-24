/* globals Chart:false, feather:false */
(function () {
  'use strict'

  // Replace feather icons
  feather.replace({ 'aria-hidden': 'true' })

  // Get the canvas context
  var ctx = document.getElementById('myChart');

  // Function to load sensor data and render chart
  async function loadSensorData() {
    try {
      const response = await fetch("/sensors");
      const result = await response.json();
      const dataRows = result.data;

      // Extract timestamps and air temperature values
      const labels = dataRows.map(row => row.timestamp);
      const airTempData = dataRows.map(row => row.air_temp);

      // Create a Chart.js line chart with the air temperature data
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Air Temperature',
            data: airTempData,
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#007bff',
            borderWidth: 4,
            pointBackgroundColor: '#007bff'
          }]
        },
        options: {
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: false
              }
            }]
          },
          legend: {
            display: true
          }
        }
      });
    } catch (error) {
      console.error("Error fetching sensor data:", error);
    }
  }

  // Load data and render chart on page load
  loadSensorData();
})();
