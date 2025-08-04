import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read your merged CSV
df = pd.read_csv(r"C:\Users\user\Desktop\Nifty50_Stock_Analysis\output\extracted_stock_data.csv")  # replace with actual path

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
