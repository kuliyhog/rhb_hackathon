from flask import Flask
from flask_cors import CORS, cross_origin
import requests
import math

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

country_balance = {
  'MYR' : 0,
  'SGD' : 0,
  'IDR' : 0,
  'THB' : 0,
  'BND' : 0,
  'KHR' : 0,
  'VND' : 0,
  'LAK' : 0
}

user_base = {
  "bob" : {
    "username" : "bob",
    "balance" : 3000000,
    "country" : "MYR"
  },
  "central_bank" : {
    "username" : "central_bank",
    "balance" : 10000000000000,
    "country" : "USD"
  },
  "merchant1" : { "username" : "merchant1",
    "balance" : 0,
    "country" : "SGD"
  },
  "merchant2" : { "username" : "merchant2",
    "balance" : 0,
    "country" : "THB"
  },
  "merchant3" : { "username" : "merchant3",
    "balance" : 0,
    "country" : "IDR"
  },
  "merchant4" : { "username" : "merchant4",
    "balance" : 0,
    "country" : "BND"
  },
  "merchant5" : { "username" : "merchant5",
    "balance" : 0,
    "country" : "KHR"
  },
  "merchant6" : { "username" : "merchant6",
    "balance" : 0,
    "country" : "VND"
  },
  "merchant7" : { "username" : "merchant7",
    "balance" : 0,
    "country" : "LAK"
  }
}


api_key = '214cfd593dc34a08acede10a254a478c'
exchange_rates = {}

def get_currency_exchange_rates():
  global exchange_rates
  if not exchange_rates:
    response = requests.get("https://openexchangerates.org/api/latest.json?app_id={}".format(api_key))
    exchange_rates = response.json()

  return exchange_rates

def deposit(username, amount):
  user_base[username]["balance"] += amount
  if username not in user_base:
    return {'status' : False, 'message' : "Please create an account first"}
  return {'status' : True, 'message' : "Deposit success"}

def withdraw(username, amount):
  user_base[username]["balance"] -= amount
  if username not in user_base:
    return {'status' : False, 'message' : "Please create an account first"}
  return {'status' : True, 'message' : "Withdraw success"}



@app.route("/get_rates")
@cross_origin()
def get_rates():
  return get_currency_exchange_rates()

@app.route("/reset_bank_balance/<int:value>")
@cross_origin()
def reset_balance(value):
  response = requests.get("https://openexchangerates.org/api/latest.json?app_id={}".format(api_key))
  rates = response.json()
  for country in country_balance:
    country_balance[country] = rates['rates'][country] * value

  return country_balance

@app.route("/get_bank_balance/<string:target_country>")
@cross_origin()
def get_balance(target_country: str):
  return str(country_balance[target_country])

@app.route("/get_bank_balance")
@cross_origin()
def get_balance_all():
  return_list = []
  for key, value in country_balance.items():
    return_list.append({'country' : key, 'balance' : value})

  return return_list

@app.route("/get_bank_balance/usd")
@cross_origin()
def get_balance_all_usd():
  return_list = []
  for key, value in country_balance.items():
    return_list.append({'country' : key, 'balance' : math.ceil(convert_currency("USD", key, value))})

  return return_list


@app.route("/create_user/<string:username>/<string:country>")
@cross_origin()
def create_user(username, country):
  if username in user_base:
    return {
      "status" : "User exists",
      "user" : user_base[username]
    }
  user_base[username] = {
    "country" : country,
    "balance" : 0
  }
  return {
    "status" : "account created!",
    "user" : user_base[username]
  }


@app.route("/get_user_balance/<string:username>")
@cross_origin()
def get_user_balance(username):
  return str(user_base[username])

@app.route("/get_users")
@cross_origin()
def get_users():
  return user_base

@app.route("/deposit/<string:username>/<int:amount>")
@cross_origin()
def deposit_funds(username, amount):
  return deposit(username, amount)

@app.route("/pay/<string:username>/<string:merchant>/<int:amount>")
@cross_origin()
def pay(username, merchant, amount):
  curr, target = user_base[username]["country"], user_base[merchant]["country"]
  curr_value = convert_currency(curr, target, amount)

  w_result = withdraw(username, curr_value)
  if not w_result['status']:
    return "Payment failed, user does not exist"
  d_result = deposit(merchant, amount)
  if not d_result['status']:
    deposit(username, curr_value)
    return "Payment target does not exist"

  adjust_bank_balance(curr, target, curr_value, amount)

  return_value = {
    'user_details' : {
      'country' : curr,
      'balance' : str(user_base[username]['balance'])
    },
    'merchant_details' :{
      'country' : target,
      'balance' : str(user_base[merchant]['balance'])
    },
    'exchange_rate' : get_conversion_rates(curr, target),
    'affected_bank_balance' : {
      curr : country_balance[curr],
      target : country_balance[target]
    },
  }
  return return_value
  
@app.route("/central_bank/topup/<string:location>/<int:value>")
@cross_origin()
def top_up(location, value):
  res = convert_currency(location, "USD", value)
  country_balance[location] += res
  user_base['central_bank']['balance'] -= value
  return {"status" : "Success", "res" : res, "value" : value}

def adjust_bank_balance(curr, target, curr_value, target_value):
  country_balance[target] -= target_value
  country_balance[curr] += curr_value

  return "True"

def get_conversion_rates(curr, target):
  rates = get_currency_exchange_rates()
  rates = rates['rates']
  return (rates[curr]/rates[target])

def convert_currency(curr, target, value):
  rates = get_conversion_rates(curr, target)
  return value*rates


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
