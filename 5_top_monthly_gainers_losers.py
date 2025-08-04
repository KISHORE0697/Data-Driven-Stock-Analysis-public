import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
final_df = pd.read_csv(r"C:\Users\user\Desktop\Nifty50_Stock_Analysis\output\extracted_stock_data.csv")

# Standardize column names
final_df.columns = final_df.columns.str.strip().str.lower()

# Check what columns are present
print(final_df.columns)

# Convert 'date' to datetime
final_df['date'] = pd.to_datetime(final_df['date'], format="%d-%m-%Y %H:%M", errors='coerce')
final_df = final_df.dropna(subset=['date'])

# Convert to month period
final_df['month'] = final_df['date'].dt.to_period('M')

# Get monthly first and last close prices
monthly_price = final_df.groupby(['stock name', 'month'])['close'].agg(['first', 'last']).reset_index()

# Calculate monthly return
monthly_price['monthly return %'] = ((monthly_price['last'] - monthly_price['first']) / monthly_price['first']) * 100

# Convert month back to datetime for plotting
monthly_price['month'] = monthly_price['month'].dt.to_timestamp()

# Check result
print(monthly_price.head())


top_5_gainers = monthly_price.sort_values(by='monthly return %', ascending=False).head(5)


plt.figure(figsize=(10,6))
sns.barplot(data=top_5_gainers, x='stock name', y='monthly return %') 
plt.title('Top 5 Monthly Gainers')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


top_5_loosers = monthly_price.sort_values(by='monthly return %', ascending=True).head(5)

plt.figure(figsize=(10,6))
sns.barplot(data=top_5_loosers, x='stock name', y='monthly return %') 
plt.title('Top 5 Monthly Losers')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()