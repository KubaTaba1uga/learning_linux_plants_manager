/* globals Chart:false, feather:false */
(function () {
  'use strict'

  // Replace feather icons
  feather.replace({ 'aria-hidden': 'true' })

  // Get the canvas context
  var air_temp_ctx = document.getElementById('air_temp');
  var air_humid_ctx = document.getElementById('air_humid');
  var soil_0_humid_ctx = document.getElementById('soil_0_humid');
    
  // Function to load sensor data and render chart
  async function loadSensorData() {
    try {
      const response = await fetch("/sensors");
      const result = await response.json();
      const dataRows = result.data;

      // Extract timestamps and air temperature values
      const labels = dataRows.map(row => row.timestamp);
      const airTempData = dataRows.map(row => row.air_temp);
      const airHumidData = dataRows.map(row => row.air_humid);
      const soil0HumidData = dataRows.map(row => row.soil_humid_0);
	
      // Create a Chart.js line chart with the air temperature data
      new Chart(air_temp_ctx, {
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
                  if (index === 0) {
                    return value;
                  } else if (index === values.length - 1) {
                    return value;
                  }
                  return '';
                }
              }
            }],
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
      // Create a Chart.js line chart with the air humidity data
      new Chart(air_humid_ctx, {
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
                  if (index === 0) {
                    return value;
                  } else if (index === values.length - 1) {
                    return value;
                  }
                  return '';
                }
              }
            }],
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
      // Create a Chart.js line chart with the air humidity data
      new Chart(soil_0_humid_ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Soil 0 Humidity',
            data: soil0HumidData,
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
                  if (index === 0) {
                    return value;
                  } else if (index === values.length - 1) {
                    return value;
                  }
                  return '';
                }
              }
            }],
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
