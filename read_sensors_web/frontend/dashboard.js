/* globals Chart:false, feather:false */
(function () {
  'use strict';

  // Replace feather icons
  feather.replace({ 'aria-hidden': 'true' });

  // Get the canvas contexts
  const air_temp_ctx = document.getElementById('air_temp');
  const air_humid_ctx = document.getElementById('air_humid');
  const soil_humid_ctx = document.getElementById('soil_humid');
  const waterings_ctx = document.getElementById('waterings');

  // Generic ChartWrapper class with built-in shared options.
  class ChartWrapper {
    static sharedOptions = {
      scales: {
        xAxes: [{
          ticks: {
            callback: (value, index, values) =>
              (index === 0 || index === values.length - 1) ? value : ''
          }
        }],
        yAxes: [{
          ticks: { beginAtZero: false }
        }]
      },
      legend: { display: true }
    };

    constructor(ctx, labels, datasets) {
      this.ctx = ctx;
      this.labels = labels;
      this.datasets = datasets;
      this.options = ChartWrapper.sharedOptions;
      this.chartInstance = null;
      this.render();
    }

    render() {
      if (this.chartInstance) {
        this.chartInstance.destroy();
      }
      const config = {
        type: 'line',
        data: {
          labels: this.labels,
          datasets: this.datasets
        },
        options: this.options
      };
      this.chartInstance = new Chart(this.ctx, config);
    }

    update(labels, datasets, options = {}) {
      this.labels = labels;
      this.datasets = datasets;
      this.render();
    }
  }

  // Global chart instances.
  let airTempChart = null;
  let airHumidChart = null;
  let soilHumidChart = null;
  let wateringsChart = null;

  async function loadSensorData(maxTimeRange) {
    let url = "/sensors";
    if (maxTimeRange) {
      url += "?max_time_range=" + maxTimeRange;
    }

    try {
      const response = await fetch(url);
      const result = await response.json();
      const dataRows = result.data;
      const labels = dataRows.map(row => row.timestamp);

      airTempChart = new ChartWrapper(air_temp_ctx, labels, [{
        label: 'Air Temperature',
        data: dataRows.map(row => row.air_temp),
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]);

      airHumidChart = new ChartWrapper(air_humid_ctx, labels, [{
        label: 'Air Humidity',
        data: dataRows.map(row => row.air_humid),
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]);

      soilHumidChart = new ChartWrapper(soil_humid_ctx, labels, [
        {
          label: 'Plant 0',
          data: dataRows.map(row => row.soil_humid_0),
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#2aff00',
          borderWidth: 4,
          pointBackgroundColor: '#2aff00'
        },
        {
          label: 'Plant 1',
          data: dataRows.map(row => row.soil_humid_1),
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#D500FF',
          borderWidth: 4,
          pointBackgroundColor: '#D500FF'
        },
        {
          label: 'Plant 2',
          data: dataRows.map(row => row.soil_humid_2),
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#20DFD1',
          borderWidth: 4,
          pointBackgroundColor: '#20DFD1'
        },
        {
          label: 'Plant 3',
          data: dataRows.map(row => row.soil_humid_3),
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#D7DF20',
          borderWidth: 4,
          pointBackgroundColor: '#D7DF20'
        }
      ]);

    } catch (error) {
      console.error("Error fetching sensor data:", error);
    }
  }

  async function loadWateringData(maxTimeRange) {
    let url = "/waterings";
    if (maxTimeRange) {
      url += "?max_time_range=" + maxTimeRange;
    }

    try {
      const response = await fetch(url);
      const result = await response.json();
      const dataRows = result.data;

      const labels = dataRows.map(row => row.timestamp);

      // Group by valve
      const valveGroups = {};
      dataRows.forEach(row => {
        const label = `Valve ${row.valve_index}`;
        if (!valveGroups[label]) {
          valveGroups[label] = [];
        }
        valveGroups[label].push({ timestamp: row.timestamp, duration: row.duration });
      });

      const datasets = Object.entries(valveGroups).map(([label, entries], index) => {
        return {
          label: label,
          data: entries.map(entry => entry.duration),
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: ['#ff6384', '#36a2eb', '#4bc0c0', '#9966ff'][index % 4],
          borderWidth: 4,
          pointBackgroundColor: ['#ff6384', '#36a2eb', '#4bc0c0', '#9966ff'][index % 4]
        };
      });

      wateringsChart = new ChartWrapper(waterings_ctx, labels, datasets);

    } catch (error) {
      console.error("Error fetching watering data:", error);
    }
  }

  window.setTimeRange = function (rangeInSeconds, label) {
    document.getElementById('timeRangeButton').innerHTML = `<span data-feather="calendar"></span> ${label}`;
    loadSensorData(rangeInSeconds);
    loadWateringData(rangeInSeconds);
  };

  // Initial load
  loadSensorData();
  loadWateringData();
})();
