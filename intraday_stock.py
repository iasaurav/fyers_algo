
# Fetch the funds information directly
response = fyers.funds()

# Extract only "Total Balance" from the response
total_balance = next((item for item in response["fund_limit"] if item["title"] == "Total Balance"), None)

# Extract equityAmount from total_balance
if total_balance:
    equity_amount = total_balance["equityAmount"]
    print(f"Available Balance: {equity_amount}")
else:
    print("Total Balance not found in the response.")

# List of orders with symbol, quantity, price, side, and type
orders = [
    {"symbol": "ACE", "qty": 1, "price": 240, "side": 1, "type": 1},
    {"symbol": "ABB", "qty": 1, "price": 112, "side": -1, "type": 1}
]

# Function to place an order
def place_order(symbol, qty, price, order_type, side):
    price = float(price)  # Ensure price is treated as a float
    data = {
        "symbol": symbol,
        "qty": qty,
        "type": order_type,  # 1 for limit order, 2 for market order
        "side": side,        # 1 for buy, -1 for sell
        "productType": "INTRADAY",
        "limitPrice": price if order_type == 1 else 0,  # Only set limitPrice if it's a limit order
        "stopPrice": 0,
        "disclosedQty": 0,
        "validity": "DAY"
    }
    # Assuming fyers.place_order() is a valid API call to place the order
    order = fyers.place_order(data)
    return order

# Loop through orders and place them if balance is sufficient
for order in orders:
    order_value = order["qty"] * float(order["price"])  # Convert price to float for the calculation
    
    # Check if equity_amount is sufficient to place the order
    if equity_amount >= order_value:
        symbol = "NSE:" + order["symbol"] + "-EQ"
        quantity = order["qty"]
        price = order["price"]
        order_type = order["type"]
        side = order["side"]
        # Place the order
        order_response = place_order(symbol, quantity, price, order_type, side)
        print(f"Order placed for {symbol}: {order_response}")
    else:
        print(f"Insufficient balance to place order for {order['symbol']}")
