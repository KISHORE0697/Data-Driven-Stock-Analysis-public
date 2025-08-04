import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load the data
df = pd.read_csv(r"C:\Users\user\Desktop\Nifty50_Stock_Analysis\output\extracted_stock_data.csv")

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Check for required columns
assert 'stock name' in df.columns and 'close' in df.columns, "Check your column names!"

# Calculate daily return
df['daily_return'] = df.groupby('stock name')['close'].pct_change()

# Drop rows where return couldn't be calculated
df = df.dropna(subset=['daily_return'])

# Calculate volatility (standard deviation of returns)
volatility_df = df.groupby('stock name')['daily_return'].std().reset_index()

# Convert to percentage and rename
volatility_df['volatility'] = volatility_df['daily_return'] * 100
volatility_df = volatility_df[['stock name', 'volatility']]

# Drop any rows with missing values
volatility_df = volatility_df.dropna()

# Sort by volatility and take top 10
top_volatile = volatility_df.sort_values(by='volatility', ascending=False).head(10)

# Print the result
print("Top 10 Most Volatile Stocks:")
print(top_volatile)

# Plotting
import matplotlib.ticker as mtick
plt.figure(figsize=(12, 6))
sns.barplot(x='stock name', y='volatility', data=top_volatile, palette='Reds')
plt.title('Top 10 Most Volatile Stocks (Standard Deviation of Daily Returns)')
plt.ylabel('Volatility (%)')
plt.xlabel('Stock Name')
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
