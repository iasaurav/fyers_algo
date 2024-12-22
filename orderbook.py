
from fyers_apiv3 import fyersModel
import pandas as pd

# Initialize the fyersModel with your client_id and access_token
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=False, log_path="")

# Fetch the funds information directly
response = fyers.funds()

# Extract only "Total Balance" from the response
total_balance = next((item for item in response["fund_limit"] if item["title"] == "Total Balance"), None)

# Extract equityAmount from total_balance
if total_balance:
    equity_amount = total_balance["equityAmount"]
    print(f"Available_Balance: {equity_amount}")
else:
    print("Total Balance not found in the response.")

# Fetch the positions data
response = fyers.positions()

# Check for netPositions in the response
if response.get("netPositions"):
    df = pd.DataFrame(response["netPositions"])
    # Selecting only the required columns
    df = df[['symbol', 'buyAvg', 'sellAvg', 'buyQty', 'sellQty', 'pl']]
    # Save to Excel
    df.to_excel("today.xlsx", index=False)
    
else:
    print("No net positions data available in the response.")

# Fetch the order book
response = fyers.orderbook()

# Check for a successful response and extract 'orderBook'
if response.get("s") == "ok" and "orderBook" in response:
    order_book = response["orderBook"]
    # Create a DataFrame from the order book data
    df_order_book = pd.DataFrame(order_book)
    # Modify the 'side' column to display 'Buy' for 1 and 'Sell' for -1
    df_order_book['side'] = df_order_book['side'].map({1: 'BUY', -1: 'SELL'})
    # Modify the 'segment' column to display 'Derivatives' for 11 and 'Commodities' for 20
    df_order_book['segment'] = df_order_book['segment'].map({10: 'STOCK',11: 'option', 20: 'option'})
    
    # Sort by 'orderDateTime' (assuming it's in a format that can be sorted like 'YYYY-MM-DD HH:MM:SS')
    if 'orderDateTime' in df_order_book.columns:
        df_order_book['orderDateTime'] = pd.to_datetime(df_order_book['orderDateTime'], errors='coerce')  # Convert to datetime
        df_order_book = df_order_book.sort_values(by='orderDateTime', ascending=False)  # Sort by orderDateTime in descending order
    
    # Selecting only the required columns
    df_order_book = df_order_book[['id', 'symbol', 'qty', 'productType', 'segment', 'side', 'orderDateTime','ex_sym']]
    
   
    # Optional: Save the DataFrame to an Excel file
    df_order_book.to_excel("order_book.xlsx", index=False)
else:
    print("Failed to fetch order book. Response:", response)
