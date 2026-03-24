# Budget Tracker

A command line budget tracking tool built with Python.

## Features
- Add income and expense transactions
- View a summary of total income, expenses, and balance
- View all transactions with category and description
- Delete transactions
- Input validation for all fields

## How to Run
Make sure Python is installed, then run:
```
python budget_tracker.py
```

## Usage
1. Add Income — log a source of income with category and description
2. Add Expense — log an expense with category and description
3. View Summary — see total income, expenses, and current balance
4. View All Transactions — see a detailed list of every transaction
5. Delete a Transaction — remove an entry by number
6. Exit

## Roadmap
The following features are planned for future development:

- **Graphical User Interface (GUI)** — add a desktop UI using Tkinter or PyQt
- **Export to Excel** — export transactions and summary to a .xlsx file using openpyxl
- **Data Persistence** — save and load transactions between sessions using JSON or CSV
- **Monthly Reports** — filter and summarize transactions by month
- **Category Breakdown** — visual charts showing spending by category using matplotlib