import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import plotly.express as px
import os   

                                # Load the cleaned dataset
df = pd.read_csv(r"C:\Users\user\Desktop\Nifty50_Stock_Analysis\output\extracted_stock_data.csv")

# Reset index to work with 'date' as a column again for clarity
df_reset = df.reset_index()

# Sort by Stock Name and Date for accurate pct_change
df_reset.sort_values(by=['Stock Name', 'date'], inplace=True)

# Calculate daily return for each stock
df_reset['daily_return'] = df_reset.groupby('Stock Name')['close'].pct_change()

# Drop NaN rows created by pct_change (first row of each group)
df_reset.dropna(subset=['daily_return'], inplace=True)

# Calculate standard deviation of daily returns per stock
volatility_df = df_reset.groupby('Stock Name')['daily_return'].std().sort_values(ascending=False)

# Get top 5 most volatile stocks
top_volatile_stocks = volatility_df.head(5).index.tolist()
print("Top 5 Most Volatile Stocks:", top_volatile_stocks)

volatile_df = df_reset[df_reset['Stock Name'].isin(top_volatile_stocks)]

plt.figure(figsize=(14, 7))
sns.lineplot(data=volatile_df, x='date', y='daily_return', hue='Stock Name', marker='o', linewidth=1.2)

plt.title("Top 5 Most Volatile Nifty 50 Stocks - Daily Return Over Time")
plt.xlabel("Date")
plt.ylabel("Daily Return")
plt.legend(title='Stock Name')
plt.grid(True)
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()