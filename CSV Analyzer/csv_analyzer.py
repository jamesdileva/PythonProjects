# CSV Data Analyzer
# Reads a CSV file and produces a summary report

import pandas as pd
import os

FILE = "sample_expenses.csv"

def load_data(filename):
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return None
    df = pd.read_csv(filename)
    print(f"\n✓ Loaded {len(df)} transactions from {filename}")
    return df

def clean_data(df):
    initial_count = len(df)
    
    # Convert amount column to numbers, any invalid values become NaN
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    
    # Remove rows with negative amounts
    df = df[df["amount"] >= 0]
    
    # Remove rows where amount is missing or invalid
    df = df.dropna(subset=["amount"])
    
    removed = initial_count - len(df)
    if removed > 0:
        print(f"⚠ {removed} invalid or incomplete rows removed from analysis.")
    
    return df

def show_summary(df):
    income = df[df["type"] == "income"]["amount"].sum()
    expenses = df[df["type"] == "expense"]["amount"].sum()
    balance = income - expenses

    print("\n--- Financial Summary ---")
    print(f"Total Income:   ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Balance:        ${balance:.2f}")

def show_category_breakdown(df):
    print("\n--- Expenses by Category ---")
    expenses = df[df["type"] == "expense"]
    breakdown = expenses.groupby("category")["amount"].sum().sort_values(ascending=False)
    for category, total in breakdown.items():
        print(f"{category:<15} ${total:.2f}")

def show_stats(df):
    expenses = df[df["type"] == "expense"]["amount"]
    print("\n--- Expense Statistics ---")
    print(f"Highest Expense: ${expenses.max():.2f}")
    print(f"Lowest Expense:  ${expenses.min():.2f}")
    print(f"Average Expense: ${expenses.mean():.2f}")
    print(f"Total Count:     {len(expenses)} transactions")

def export_report(df):
    income = df[df["type"] == "income"]["amount"].sum()
    expenses = df[df["type"] == "expense"]["amount"].sum()
    balance = income - expenses
    expense_df = df[df["type"] == "expense"]
    breakdown = expense_df.groupby("category")["amount"].sum().sort_values(ascending=False)

    with open("report.txt", "w") as f:
        f.write("=== Financial Report ===\n\n")
        f.write(f"Total Income:   ${income:.2f}\n")
        f.write(f"Total Expenses: ${expenses:.2f}\n")
        f.write(f"Balance:        ${balance:.2f}\n")
        f.write("\n--- Expenses by Category ---\n")
        for category, total in breakdown.items():
            f.write(f"{category:<15} ${total:.2f}\n")

    print("\n✓ Report exported to report.txt")

def main():
    print("Welcome to CSV Analyzer")
    df = load_data(FILE)
    if df is None:
        return
    df = clean_data(df)  # ADD THIS LINE

    while True:
        print("\nWhat would you like to do?")
        print("1. View Financial Summary")
        print("2. View Category Breakdown")
        print("3. View Expense Statistics")
        print("4. Export Report to File")
        print("5. Exit")

        choice = input("\nEnter choice (1-5): ")

        if choice == "1":
            show_summary(df)
        elif choice == "2":
            show_category_breakdown(df)
        elif choice == "3":
            show_stats(df)
        elif choice == "4":
            export_report(df)
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please enter 1-5.")

main()
