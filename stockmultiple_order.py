

#multiple_order


# Example: List of orders with symbol, quantity, price, side, and type
orders = [
    {"symbol": "ACE", "qty": 10, "price": 2400, "side": 1, "type": 1},
    {"symbol": "ABB", "qty": 100, "price": 0, "side": -1, "type": 1}
]

# Function to place an order
def place_order(symbol, qty, price, order_type, side):
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

# Place multiple orders
for order in orders:
    symbol = "NSE:" + order["symbol"] + "-EQ"
    quantity = order["qty"]
    price = order["price"]
    order_type = order["type"]
    side = order["side"]
    # Place each order
    order_response = place_order(symbol, quantity, price, order_type, side)
    print(f"Order placed for {symbol}: {order_response}")