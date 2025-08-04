import pandas as pd

df = pd.read_csv("C:/Users/user/Desktop/Nifty50_Stock_Analysis/output/extracted_stock_data_with_sector.csv")

df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date'])

df_sorted = df.sort_values(by=['Stock Name', 'date'])

# Get first and last close price per stock
first_close = df_sorted.groupby('Stock Name').first()['close']
last_close = df_sorted.groupby('Stock Name').last()['close']

# Calculate return
returns = ((last_close - first_close) / first_close) * 100
returns_df = pd.DataFrame({
    'Stock Name': returns.index,
    'Yearly Return (%)': returns.values
})

# Merge sector info (from original file)
sector_map = df[['Stock Name', 'Sector']].drop_duplicates()
returns_df = returns_df.merge(sector_map, on='Stock Name', how='left')

# Top 10 Green
top_green = returns_df.sort_values(by='Yearly Return (%)', ascending=False).head(10)

# Top 10 Loss
top_loss = returns_df.sort_values(by='Yearly Return (%)').head(10)

# Market Summary
green_count = (returns_df['Yearly Return (%)'] > 0).sum()
red_count = (returns_df['Yearly Return (%)'] <= 0).sum()

average_price = df['close'].mean()
average_volume = df['volume'].mean()

# Display results
print("\n Top 10 Green Stocks:")
print(top_green)

print("\n Top 10 Loss Stocks:")
print(top_loss)

print("\n Market Summary:")
print(f"Green Stocks: {green_count}")
print(f"Red Stocks: {red_count}")
print(f"Average Closing Price: {average_price:.2f}")
print(f"Average Volume: {average_volume:.2f}")


###################   ----- VOLATILITY ANALYSIS -----   ###################

import matplotlib.pyplot as plt

# Drop any rows with missing values in 'close' or 'Stock Name'
df.dropna(subset=['close', 'Stock Name'], inplace=True)

# Sort the data by Stock Name and date
df.sort_values(by=['Stock Name', 'date'], inplace=True)

# Calculate daily returns for each stock
df['daily_return'] = df.groupby('Stock Name')['close'].pct_change()

volatility = df.groupby('Stock Name')['daily_return'].std().reset_index()
volatility.columns = ['Stock Name', 'volatility']


top_10_volatile = volatility.sort_values(by='volatility', ascending=False).head(10)

###*********** Plot the BAR chart *****###########
plt.figure(figsize=(12, 6))
plt.bar(top_10_volatile['Stock Name'], top_10_volatile['volatility'] * 100, color='Blue')  # convert to %
plt.title('Top 10 Most Volatile Nifty 50 Stocks (1-Year)')
plt.xlabel('Stock Name')
plt.ylabel('Volatility (% of Daily Returns)')  # updated label
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

###################   ----- Cumulative Return Over Time: -----   ###################

df['first_day_price'] = df.groupby('Stock Name')['close'].transform('first')

# Step 2: Calculate cumulative return
df['cumulative_return'] = (df['close'] / df['first_day_price']) - 1

# Step 3: Get final cumulative return for each stock (last date)
final_returns = df.groupby(['Stock Name'])['cumulative_return'].last().reset_index()

# Step 4: Get top 5 stocks based on final cumulative return
top_5 = final_returns.sort_values(by='cumulative_return', ascending=False).head(5)

# Step 5: Filter data for only those top 5 stocks
top_5_symbols = top_5['Stock Name'].tolist()
top_5_data = df[df['Stock Name'].isin(top_5_symbols)]

# Step 6: Plot line chart (one line for each stock)
plt.figure(figsize=(14, 6))
for symbol in top_5_symbols:
    stock_data = top_5_data[top_5_data['Stock Name'] == symbol]
    stock_name = stock_data['Stock Name'].iloc[0]
    plt.plot(stock_data['date'], stock_data['cumulative_return'], label=stock_name)

plt.title("Cumulative Return Over Time - Top 5 Performing Stocks", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

###################   ----- Sector-wise Performance: -----   ###################

import pandas as pd
import matplotlib.pyplot as plt

stock_returns_df = pd.read_csv("C:/Users/user/Desktop/Nifty50_Stock_Analysis/output/stock_returns.csv")  

sector_df = pd.read_csv("C:/Users/user/Desktop/Nifty50_Stock_Analysis/output/extracted_stock_data_with_sector.csv")

# ✅ Clean column names and values
stock_returns_df.columns = stock_returns_df.columns.str.strip()
sector_df.columns = sector_df.columns.str.strip()
stock_returns_df['Stock Name'] = stock_returns_df['Stock Name'].astype(str).str.strip()
sector_df['Stock Name'] = sector_df['Stock Name'].astype(str).str.strip()

# Merge sector data
merged_df = pd.merge(stock_returns_df, sector_df, on='Stock Name', how='left')

# Group by sector and calculate mean return
sector_perf = merged_df.groupby('Sector')['yearly_return'].mean().reset_index()

# Sort sectors by average return for better visualization
sector_perf = sector_perf.sort_values(by='yearly_return', ascending=False)

# Plot
plt.figure(figsize=(12, 6))
plt.bar(sector_perf['Sector'], sector_perf['yearly_return'] * 100, color='skyblue')  # convert to %

plt.title('Average Yearly Return by Sector (Nifty 50)')
plt.xlabel('Sector')
plt.ylabel('Average Yearly Return (%)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


################**************Stock Price Correlation*****************###################

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read your merged CSV
df = pd.read_csv(r"C:/Users/user/Desktop/Nifty50_Stock_Analysis/output/stock_returns.csv")  # replace with actual path

# Ensure 'date', 'symbol', and 'close' columns exist
print(df.columns)

# Convert 'date' column to datetime if not done yet
df['date'] = pd.to_datetime(df['date'], format="%d-%m-%Y %H:%M", errors='coerce')

# Pivot the table: rows = date, columns = stock symbol, values = closing price
pivot_df = df.pivot_table(index='date', columns='Stock Name', values='close')

# Drop rows with NaNs to avoid skewed correlation
pivot_df = pivot_df.dropna()

print(pivot_df.head())

# Correlation matrix
correlation_matrix = pivot_df.corr()

# Plot heatmap
plt.figure(figsize=(16, 12))
sns.heatmap(correlation_matrix, cmap='coolwarm', annot=False, linewidths=0.5)
plt.title("Stock Correlation Heatmap (Based on Close Prices)")
plt.tight_layout()
plt.show()


################**************TO 5 MONTLY GAINERS AND LOOSERS *****************###################

