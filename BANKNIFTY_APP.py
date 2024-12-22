#BANKNIFTY
import requests
import csv
from io import StringIO
index_name = "BANKNIFTY"
quantity = 1

# CSV URL
data_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQs5smrso2vUZEi3tTjUGShzukMDn8SwlKM0A4GOOr11iOe788-4SV2a774nFpsNN-3wGlYw-Ah3J7T/pub?gid=1157342848&single=true&range=J1:N10&output=csv"

def get_trading_code_and_tyers(index_name):
    try:
        # Fetch the CSV content
        response = requests.get(data_url)
        
        # Ensure the request was successful
        response.raise_for_status()  # This will raise an exception for HTTP errors
        
        # Read CSV data
        csv_data = StringIO(response.text)
        reader = csv.DictReader(csv_data)

        # Loop through the rows and find the matching index
        for row in reader:
            if row["name"].lower() == index_name.lower():
                # Return both trading_code, tyers, and lot_size
                return row["trading_code"], row["tyers"], row["lot_size"]
        
        return "Index not found", None, None  # Return None for tyers and lot_size if index not found
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}", None, None  # Handle request errors

# Example usage

trading_code, tyers, lot_size = get_trading_code_and_tyers(index_name)
if trading_code != "Index not found":

    print(f"Trading code for {index_name}: {trading_code}, Tyers: {tyers}, Lot size: {lot_size}")
else:
    print(f"{index_name} not found")


ticker_expiry = trading_code
ticker = tyers
lot = lot_size

#print(ticker_expiry)
#print(tyers)
#print(lot)


#don't change 





trade_quantity_lot_size = float(quantity) * int(lot)






# Import datetime here to ensure it's available in this scope
from datetime import datetime, timedelta 
# Reformat expiry date


# Modify the ticker to remove "-INDEX"
modified_ticker = ticker.replace("-INDEX", "")

# Prepare the base result format with expiry and strike price placeholder
result = ticker_expiry


# Time setup
today = datetime.now()
previous_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")  # Fetching 1 day of data
current_date = today.strftime("%Y-%m-%d")



#FYERS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fyers_apiv3 import fyersModel
file_name = '/content/drive/MyDrive/ALGO/FYERS/fyers_access_token.txt'
exec(open(file_name).read())

 


# Initialize the FyersModel instance
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")



# Data fetching
data = {
    "symbol": ticker,
    "resolution": "5",
    "date_format": "1",
    "range_from": previous_date,
    "range_to": current_date,
    "cont_flag": "1"
}

response = fyers.history(data=data)

if response["s"] != "ok":
    print("Error fetching data:", response)
    exit()

# Convert the fetched data to a Pandas DataFrame
historical_data = pd.DataFrame(response["candles"], columns=["timestamp", "open", "high", "low", "close", "volume"])
historical_data["timestamp"] = pd.to_datetime(historical_data["timestamp"], unit="s")

# Calculate EMA for different periods
for period in [9, 20, 50, 200]:
    historical_data[f"ema_{period}"] = historical_data["close"].ewm(span=period, adjust=False).mean()

# Get the latest row for comparison
latest_data = historical_data.iloc[-1]
LTP = latest_data["close"]

# Round LTP to nearest hundred for strike price
trade = int(round(LTP, -2))

print(f"Latest Traded Price (LTP): {LTP}")
print(f"Strike Price: {trade}")

# Compare LTP with EMAs to generate a signal
if LTP > latest_data["ema_9"] and LTP > latest_data["ema_20"]:
    signal = f"{result}{trade}CE"  # CE for Call option
elif LTP > latest_data["ema_50"] and LTP > latest_data["ema_200"]:
    signal = f"{result}{trade}PE"  # PE for Put option
else:
    signal = "No Trade"

# Output the signal
print(f"Signal: {signal}")


# Request data
data = {
    "symbols": signal
}

# Fetch quotes
response = fyers.quotes(data=data)

# Check response
if response["s"] == "ok":
    for symbol_data in response["d"]:
        symbol = symbol_data["n"]
        last_price = symbol_data["v"]["lp"]
        current = last_price * trade_quantity_lot_size

        print(f"Symbol: {symbol}, Last Price (lp): {last_price}\n{current}")
else:
    print("Failed to fetch quotes:", response)

# Get the funds information
response = fyers.funds()

# Extract and print Total Balance
total_balance = next(
    (item["equityAmount"] for item in response["fund_limit"] if item["title"] == "Total Balance"), None
)
print(f"Total Balance (Equity): {total_balance}")

# Check if Total Balance is greater than 'current' before placing the order
if total_balance and total_balance > current:
    # Place the order using the generated signal
    data = {
        "symbol": signal,  # The symbol to trade
        "qty": trade_quantity_lot_size,  # Number of contracts (adjust as needed)
        "type": 1,  # Order type: 2 for limit order
        "side": 1,  # 1 for Buy, -1 for Sell
        "productType": "INTRADAY",  # Product type: Intraday trade
        "limitPrice": last_price-50,  # Limit price (use 0 for market price)
        "stopPrice": 0,  # Stop price (use 0 for no stop)
        "validity": "DAY",  # Validity of the order
        "disclosedQty": 0,  # Disclosed quantity (optional)
        "offlineOrder": False,  # Offline order flag
        "orderTag": "tag1"  # Optional order tag
    }

    # Place the order
    response = fyers.place_order(data=data)
    print("Order Response:", response)
else:
    print("Insufficient balance. Order not placed.")
    print(f"Required Balance: {current}, Available Balance: {total_balance}")