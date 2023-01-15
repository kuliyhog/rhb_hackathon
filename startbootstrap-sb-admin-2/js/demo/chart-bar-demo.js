// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Bar Chart Example
async function fetchData(link) {
  var response_data;
  await fetch(link)
  .then((response) => response.json())
  .then((data) => response_data = data);
  return response_data;
}

updateData();
var country_labels = [];
var country_labels = [];
var ctx = document.getElementById("country_balance");
var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: country_labels,
    datasets: [{
      label: "Revenue",
      backgroundColor: "#4e73df",
      hoverBackgroundColor: "#2e59d9",
      borderColor: "#4e73df",
      data: country_balance,
    }],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 8
        },
        maxBarThickness: 25,
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: 150000,
          maxTicksLimit: 5,
          padding: 10,
        },
        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false
    },
    tooltips: {
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
  }
});


function updateData(){
  var response_data = fetchData('http://localhost:5000/get_bank_balance/usd')
  .then(datapoints => {
      const country_labels = datapoints.map(datapoint => {
        return datapoint.country;
      });
      const country_balance = datapoints.map(datapoint => {
        return datapoint.balance;
      });
      myBarChart.data.labels = country_labels;
      myBarChart.data.datasets[0].data = country_balance;
      myBarChart.update();
    })
}
