import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os   

# STEP 1: Load the data
stock_df = pd.read_csv("C:/Users/user/Desktop/Nifty50_Stock_Analysis/output/extracted_stock_data.csv")
sector_df = pd.read_csv("C:/Users/user/Desktop/Nifty50_Stock_Analysis/output/Sector_data.csv")

stock_df['Stock Name'] = stock_df['Stock Name'].str.strip().str.upper()
sector_df['Symbol'] = sector_df['Symbol'].str.strip().str.upper()

merged_df = stock_df.merge(sector_df, left_on='Stock Name', right_on='Symbol', how='left')

null_sectors = merged_df[merged_df['Sector'].isnull()]

if null_sectors.empty:
    print("✅ All stocks successfully mapped to sectors.")
else:
    print("⚠️ Warning: These stocks have missing sectors:")
    if 'Stock Name' in null_sectors.columns:
        print(null_sectors['Stock Name'].drop_duplicates())
    else:
        print("Available columns:", null_sectors.columns)

print(null_sectors['Stock Name_x'].drop_duplicates())

merged_df.to_csv("nifty50_with_sectors.csv", index=False)

df = pd.read_csv("C:/Users/user/Desktop/Nifty50_Stock_Analysis/output/merged_stock_data.csv")

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

# Extract year
df['year'] = df['date'].dt.year

# Filter for full year only (latest year, e.g. 2024)
latest_year = df['year'].max()
year_df = df[df['year'] == latest_year]

# Group by Stock to get first and last close of the year
returns = year_df.sort_values(['Stock Name', 'date']).groupby('Stock Name').agg(
    first_close=('close', 'first'),
    last_close=('close', 'last'),
    Sector=('Sector', 'first')  # Get sector too
).reset_index()

# Calculate yearly return (%)
returns['Yearly Return'] = ((returns['last_close'] - returns['first_close']) / returns['first_close']) * 100


# Group by Sector to get average return
sector_avg = returns.groupby('Sector')['Yearly Return'].mean().reset_index()

# Sort for better visuals
sector_avg = sector_avg.sort_values(by='Yearly Return', ascending=False)

# Plot
plt.figure(figsize=(12,6))
sns.barplot(data=sector_avg, x='Sector', y='Yearly Return', palette='viridis')

plt.title('Average Yearly Return by Sector (2024)', fontsize=14)
plt.xlabel('Sector')
plt.ylabel('Average Yearly Return (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


