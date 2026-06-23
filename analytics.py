import pandas as pd
import matplotlib.pyplot as plt
def filter_category(df):
    search = input("Enter category to filter by: ").strip().lower()
    if not search:
        print("Error: Search term cannot be empty.")
        return
    filter_df=df[df['category'].str.lower() == search]
    if not filter_df.empty:
        print(filter_df)
    else:
        print("No expenses found in this category.")
def filter_date(df):
    search = input("Enter date or month to filter (e.g., '2026-05'): ").strip()
    if not search:
        print("Error: Search term cannot be empty.")
        return
    filter_df = df[df['date'].str.contains(search)]
    if not filter_df.empty:
        print(filter_df)
    else:
        print(f"No expenses found matching '{search}'.")
def filter_amount(df):
    try:
        amount_input = input("Enter amount to filter: ").strip()
        if not amount_input:
            return
        value = float(amount_input)
    except ValueError:
        print("Error: Please enter a valid number.")
        return 
    filter_df=df[df['amount'] == value]
    if not filter_df.empty:
        print(filter_df)
    else:
        print(f"No expenses found with amount ${value}")
def check_data_completeness(df):
    print("\n--- Data Completeness Check ---")
   
    incomplete = df[df.isnull().any(axis=1)]

    if incomplete.empty:
        print("OK: All data entries are complete!")
    else:
        print("WARNING: These rows have missing data:")
        print(incomplete)
def plot_category_pie(df):
    if df.empty:
        print('No data to plot!')
        return
    category_total = df.groupby('category')['amount'].sum()
    plt.figure(figsize=(8,6))
    category_total.plot(kind='pie', autopct='%1.1f%%',startangle=140)
    plt.title("Spending by category")
    plt.ylabel("")
    plt.show()
def plot_daily_bar(df):
    if df.empty:
        print("No data to plot!")
        return
    plot_df=df.copy()
    daily_totals = plot_df.groupby('date')['amount'].sum().tail(7)
    plt.figure(figsize=(10,5))
    daily_totals.plot(kind='bar',color='skyblue',edgecolor='black')
    plt.title("Daily Spending (Last 7 Days)")
    plt.xlabel("Date")
    plt.ylabel("Amount Spend ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
