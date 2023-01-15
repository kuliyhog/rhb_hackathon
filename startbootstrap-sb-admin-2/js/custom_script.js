async function fetchData(link) {
  var response_data;
  await fetch(link)
  .then((response) => response.json())
  .then((data) => response_data = data);

  return response_data;
}


async function processPayment() {
  var user = document.getElementById("payment_user").value;
  var merchant = document.getElementById("payment_merchant").value;
  var amount = document.getElementById("payment_amount").value;
  var response = fetchData('http://localhost:5000/pay/' + user + '/' + merchant + '/' + amount)
  .then(status => {
    var user_balance = status['user_details']['balance'] + " " + status['user_details']['country']
    var merchant_balance = status['merchant_details']['balance'] + " " + status['merchant_details']['country']

    var return_text = "User Balance: " + user_balance + "<br>Merchant Balance: " + merchant_balance + "<br>Exchange Rate: " + status['exchange_rate']
    $('.modal-title').html("Transaction Details");
    $('.modal-body').html(return_text);
    $("#myModal").modal();
    processBalances();
  })
}

async function processBalances(){
  var response = fetchData('http://localhost:5000/get_users')
  .then(datapoints => {
    for (var key in datapoints){
      document.getElementById(key).innerHTML = datapoints[key].country + " " + datapoints[key].balance;
    }
  })  
}

async function centralBankTopup(){
  var target_bank = document.getElementById('top_up_select_value').value;
  var amount = document.getElementById('top_up_amount').value;
  var response = fetchData('http://localhost:5000/central_bank/topup/' + target_bank + '/' + amount)
  .then(response => {
    alert(response.status);
  })  
}