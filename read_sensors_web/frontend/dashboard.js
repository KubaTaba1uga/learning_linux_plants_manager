/* globals Chart:false, feather:false */
(function () {
  'use strict'

  // Replace feather icons
  feather.replace({ 'aria-hidden': 'true' })

  // Get the canvas context
  var air_temp_ctx = document.getElementById('air_temp');
  var air_humid_ctx = document.getElementById('air_humid');
  var soil_humid_ctx = document.getElementById('soil_humid');
    
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


	
      // Create a Chart.js line chart with the soil humidity data
      new Chart(soil_humid_ctx, {
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
          },{
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
          }, ]
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
