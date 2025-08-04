import os
import pandas as pd

# ✅ Folder containing all cleaned stock CSVs
folder_path = r"C:\Users\user\Desktop\Nifty50_Stock_Analysis\output"

# ✅ List to hold all individual stock DataFrames
all_dataframes = []

# ✅ Loop through files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path)
        df['Stock'] = file_name.replace('.csv', '')  # Add stock name column
        all_dataframes.append(df)

# ✅ Merge all DataFrames into one
merged_df = pd.concat(all_dataframes, ignore_index=True)

# ✅ Save merged data to CSV
merged_path = r"C:\Users\user\Desktop\Nifty50_Stock_Analysis\merged_stock_data.csv"
merged_df.to_csv(merged_path, index=False)

print("✅ Merged file saved at:", merged_path)
