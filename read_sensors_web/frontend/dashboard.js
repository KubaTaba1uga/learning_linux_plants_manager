/* globals Chart:false, feather:false */
(function () {
  'use strict';

  // Replace feather icons
  feather.replace({ 'aria-hidden': 'true' });

  // Get the canvas contexts
  var air_temp_ctx = document.getElementById('air_temp');
  var air_humid_ctx = document.getElementById('air_humid');
  var soil_humid_ctx = document.getElementById('soil_humid');

  // Global variables to store Chart instances
  let airTempChart = null;
  let airHumidChart = null;
  let soilHumidChart = null;

  // Function to load sensor data and render charts with an optional maxTimeRange (in seconds)
  async function loadSensorData(maxTimeRange) {
    // Build the API URL based on time range selection.
    let url = "/sensors";
    if (maxTimeRange) {
      url += "?max_time_range=" + maxTimeRange;
    }
    
    try {
      const response = await fetch(url);
      const result = await response.json();
      const dataRows = result.data;

      // Extract labels and datasets
      const labels = dataRows.map(row => row.timestamp);
      const airTempData = dataRows.map(row => row.air_temp);
      const airHumidData = dataRows.map(row => row.air_humid);

      // Destroy existing charts if they exist
      if (airTempChart) {
        airTempChart.destroy();
      }
      if (airHumidChart) {
        airHumidChart.destroy();
      }
      if (soilHumidChart) {
        soilHumidChart.destroy();
      }

      // Create/update Air Temperature chart
      airTempChart = new Chart(air_temp_ctx, {
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
            xAxes: [{
              ticks: {
                callback: function(value, index, values) {
                  return (index === 0 || index === values.length - 1) ? value : '';
                }
              }
            }],
            yAxes: [{
              ticks: {
                beginAtZero: false
              }
            }]
          },
          legend: { display: true }
        }
      });

      // Create/update Air Humidity chart
      airHumidChart = new Chart(air_humid_ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Air Humidity',
            data: airHumidData,
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#007bff',
            borderWidth: 4,
            pointBackgroundColor: '#007bff'
          }]
        },
        options: {
          scales: {
            xAxes: [{
              ticks: {
                callback: function(value, index, values) {
                  return (index === 0 || index === values.length - 1) ? value : '';
                }
              }
            }],
            yAxes: [{
              ticks: {
                beginAtZero: false
              }
            }]
          },
          legend: { display: true }
        }
      });

      // Create/update Soil Humidity chart
      soilHumidChart = new Chart(soil_humid_ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Plant 0',
            data: dataRows.map(row => row.soil_humid_0),
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#2aff00',
            borderWidth: 4,
            pointBackgroundColor: '#2aff00'
          }, {
            label: 'Plant 1',
            data: dataRows.map(row => row.soil_humid_1),
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#D500FF',
            borderWidth: 4,
            pointBackgroundColor: '#D500FF'
          }, {
            label: 'Plant 2',
            data: dataRows.map(row => row.soil_humid_2),
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#20DFD1',
            borderWidth: 4,
            pointBackgroundColor: '#20DFD1'
          }, {
            label: 'Plant 3',
            data: dataRows.map(row => row.soil_humid_3),
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#D7DF20',
            borderWidth: 4,
            pointBackgroundColor: '#D7DF20'
          }]
        },
        options: {
          scales: {
            xAxes: [{
              ticks: {
                callback: function(value, index, values) {
                  return (index === 0 || index === values.length - 1) ? value : '';
                }
              }
            }],
            yAxes: [{
              ticks: {
                beginAtZero: false
              }
            }]
          },
          legend: { display: true }
        }
      });

    } catch (error) {
      console.error("Error fetching sensor data:", error);
    }
  }

  // Function called on dropdown selection to set the time range and update charts
  window.setTimeRange = function(rangeInSeconds, label) {
    // Optionally update the button text
    document.getElementById('timeRangeButton').innerHTML = `<span data-feather="calendar"></span> ${label}`;
    // Re-render charts with the new time range
    loadSensorData(rangeInSeconds);
  };

  // Initial load with default time range (optional)
  loadSensorData();
})();
