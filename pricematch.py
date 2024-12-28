#placeorderiflast_price=price

from fyers_apiv3 import fyersModel

client_id = "XC4XXXXM-100"
access_token = "eyJ0eXXXXXXXX2c5-Y3RgS8wR14g"

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=False, log_path="")

# Example: List of orders with symbol, quantity, price, side, and type
orders = [
    {"symbol": "ACE", "qty": 10, "price": 2400, "side": 1, "type": 1},
    {"symbol": "ABB", "qty": 100, "price": 220, "side": -1, "type": 1}
]

# Function to get last price of the symbol
def get_last_price(symbol):
    try:
        response = fyers.quotes(data={"symbols": symbol})
        last_price = response["d"][0]["v"]["lp"]
        return last_price
    except Exception as e:
        print(f"Error fetching last price for {symbol}: {e}")
        return None

# Function to place an order
def place_order(symbol, qty, price, order_type, side):
    data = {
        "symbol": symbol,
        "qty": qty,
        "type": order_type,  # 1 for limit order, 2 for market order
        "side": side,        # 1 for buy, -1 for sell
        "productType": "INTRADAY",
        "limitPrice": price,  # Set the limitPrice directly to the price
        "stopPrice": 0,
        "disclosedQty": 0,
        "validity": "DAY"
    }
    # Assuming fyers.place_order() is a valid API call to place the order
    order = fyers.place_order(data)
    return order

# Place multiple orders
for order in orders:
    symbol = "NSE:" + order["symbol"] + "-EQ"
    quantity = order["qty"]
    price = order["price"]
    order_type = order["type"]
    side = order["side"]
    
    # Get the last price of the symbol
    last_price = get_last_price(symbol)

    # Place the order only if the last price matches the order price
    if last_price and last_price == price:
        order_response = place_order(symbol, quantity, price, order_type, side)
        print(f"Order placed for {symbol}: {order_response}")
    else:
        print(f"Last price for {symbol} does not match order price. No order placed.")
