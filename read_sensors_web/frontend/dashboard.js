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

  const plantColors = ['#2aff00', '#D500FF', '#20DFD1', '#D7DF20'];

  class ChartWrapper {
    static sharedOptions = {
      scales: {
        xAxes: [{
          ticks: {
            callback: (value, index, values) =>
              (index === 0 || index === values.length - 1) ? value : ''
          },
          stacked: false
        }],
        yAxes: [{
          ticks: { beginAtZero: false },
          stacked: false
        }]
      },
      legend: { display: true }
    };

    constructor(ctx, labels, datasets, type = 'line') {
      this.ctx = ctx;
      this.labels = labels;
      this.datasets = datasets;
      this.type = type;
      this.options = ChartWrapper.sharedOptions;
      this.chartInstance = null;
      this.render();
    }

    render() {
      if (this.chartInstance) {
        this.chartInstance.destroy();
      }
      const config = {
        type: this.type,
        data: {
          labels: this.labels,
          datasets: this.datasets
        },
        options: this.options
      };
      this.chartInstance = new Chart(this.ctx, config);
    }

    update(labels, datasets, type = this.type) {
      this.labels = labels;
      this.datasets = datasets;
      this.type = type;
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
          borderColor: plantColors[0],
          borderWidth: 4,
          pointBackgroundColor: plantColors[0]
        },
        {
          label: 'Plant 1',
          data: dataRows.map(row => row.soil_humid_1),
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: plantColors[1],
          borderWidth: 4,
          pointBackgroundColor: plantColors[1]
        },
        {
          label: 'Plant 2',
          data: dataRows.map(row => row.soil_humid_2),
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: plantColors[2],
          borderWidth: 4,
          pointBackgroundColor: plantColors[2]
        },
        {
          label: 'Plant 3',
          data: dataRows.map(row => row.soil_humid_3),
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: plantColors[3],
          borderWidth: 4,
          pointBackgroundColor: plantColors[3]
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

      // Group by valve/plant
      const valveGroups = {};
      dataRows.forEach(row => {
        const label = `Plant ${row.valve_index}`;
        if (!valveGroups[label]) {
          valveGroups[label] = [];
        }
        valveGroups[label].push(row.duration);
      });

      const datasets = Object.entries(valveGroups).map(([label, data], index) => {
        const plantIndex = parseInt(label.split(" ")[1]);
        return {
          label: label,
          data: data,
          backgroundColor: plantColors[plantIndex % plantColors.length],
          borderWidth: 1
        };
      });

      wateringsChart = new ChartWrapper(waterings_ctx, labels, datasets, 'bar');

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
