#advance_stoploss
from fyers_apiv3 import fyersModel
import requests
import csv
from io import StringIO
# Load credentials
exec(open('/content/drive/MyDrive/ALGO/FYERS/fyers_access_token.txt').read())

# Input from the user
inp = input("Enter the symbol: NSE:BANKNIFTY24DEC49300CE")
quantity = 1 # Quantity in lots
percentage = 10  # Percentage for stoploss calculation

# Process the input string to extract the symbol
def process_string(input_string):
    input_string = input_string[4:]
    for keyword in ['NIFTY', 'BANKNIFTY', 'FINNIFTY', 'SENSEX', 'BANKEX', 'CRUDEOIL']:
        if keyword in input_string:
            return input_string.split(keyword)[0] + keyword
    return input_string

# Fetch lot size from a CSV file
def get_lot_size(symbol):
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQs5smrso2vUZEi3tTjUGShzukMDn8SwlKM0A4GOOr11iOe788-4SV2a774nFpsNN-3wGlYw-Ah3J7T/pub?gid=1157342848&single=true&range=J1:N10&output=csv"
    try:
        response = requests.get(url)
        response.raise_for_status()
        reader = csv.DictReader(StringIO(response.text))
        return next((int(row["lot_size"]) for row in reader if row["name"].lower() == symbol.lower()), None)
    except Exception as e:
        print(f"Error fetching lot size: {e}")
        return None

# Initialize Fyers

fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=False, log_path="")

# Fetch last price
response = fyers.quotes(data={"symbols": inp})
last_price = response["d"][0]["v"]["lp"] if response["s"] == "ok" else 0

# Calculating stop losses
stoploss1 = round(last_price - last_price * (percentage / 100)-1)  # rounding to nearest 10
stoploss2 = round(last_price - last_price * (percentage / 100))  # rounding to nearest 10

# Process input and calculate lot size
symbol = process_string(inp)
lot_size = get_lot_size(symbol)
trade_quantity = quantity * lot_size if lot_size else 1

# Prepare stop-loss order data
order_data = {
    "symbol": inp,
    "qty": trade_quantity,
    "type": 4,
    "side": -1,
    "productType": "INTRADAY",
    "limitPrice": stoploss1,
    "stopPrice": stoploss2,
    "validity": "DAY",
    "disclosedQty": 0,
    "offlineOrder": False,
    "orderTag": "fyersapi"
}

# Place the order
response = fyers.place_order(order_data)
print(response)

# Print the stop-loss details
print(f"Current price: {last_price}\nLimit price: {stoploss1}, Stop price: {stoploss2}")

# Calculation of difference in percentage