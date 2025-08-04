import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(layout="wide", page_title="Nifty50 Stock Analysis Dashboard")

# Title
st.title("📊 Nifty50 Stock Analysis Dashboard")
st.markdown("Use the filters on the left to explore stock performance by sector.")

# Load the dataset
df = pd.read_csv(r"C:\Users\user\Desktop\Nifty50_Stock_Analysis\merged_stock_data_with_analysis.csv")

# Debug: Show available column names
st.write("✅ **Available Columns in Data:**")
st.write(df.columns.tolist())

# OPTIONAL: If your column is not 'Volatility (%)', rename it accordingly
# For example, if actual column is 'Volatility', rename it
if 'Volatility' in df.columns and 'Volatility (%)' not in df.columns:
    df.rename(columns={'Volatility': 'Volatility (%)'}, inplace=True)

# Sidebar filters
sectors = df['Sector'].unique()
selected_sectors = st.sidebar.multiselect("Select Sector(s)", sectors, default=sectors)

filtered_df = df[df['Sector'].isin(selected_sectors)]

# Display filtered raw data
st.subheader(f"Showing data for {filtered_df['Stock Name'].nunique()} selected stock(s) in {len(selected_sectors)} sector(s)")
st.dataframe(filtered_df)

# Check if 'Volatility (%)' exists before accessing
if 'Volatility (%)' in filtered_df.columns:
    # Display top volatile stocks
    volatility_data = filtered_df[['Stock Name', 'Volatility (%)']].drop_duplicates()
    top_volatile = volatility_data.sort_values(by='Volatility (%)', ascending=False).head(10)

    st.subheader("🔥 Top 10 Most Volatile Stocks")
    st.dataframe(top_volatile)

    # Bar plot for volatility
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=top_volatile, x='Volatility (%)', y='Stock Name', palette='coolwarm', ax=ax)
    ax.set_title("Top 10 Most Volatile Stocks")
    st.pyplot(fig)
else:
    st.warning("Required column `'Volatility (%)'` not found in the dataset.")
