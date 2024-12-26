

from fyers_apiv3 import fyersModel

# Load credentials
exec(open('/content/drive/MyDrive/ALGO/FYERS/fyers_access_token.txt').read())

# Initialize FyersModel
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=True)
symbol= "NSE:NIFTY24DEC23850CE"
# Fetch quotes for live symbol and print last price
last_price = fyers.quotes(data={"symbols": symbol})["d"][0]["v"]["lp"]
p=round(last_price)*20/100
cp=last_price-p
print(f"c{last_price}")