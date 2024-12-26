
from fyers_apiv3 import fyersModel
import pandas as pd

# Load credentials
exec(open('/content/drive/MyDrive/ALGO/FYERS/fyers_access_token.txt').read())

# Initialize Fyers API
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")

# Fetch positions data
response = fyers.positions()

# Extract 'overall' data from the response
overall_data = response.get('overall', {})
# Convert the 'overall' data to a DataFrame
df_overall = pd.DataFrame([overall_data])
df_overall = df_overall[['pl_total','pl_realized','pl_unrealized']]
df_overall.to_excel('net_proit_Loss.xlsx', index=False)

print(f"net_proit_Loss.xlsx data saved ")
print(df_overall)