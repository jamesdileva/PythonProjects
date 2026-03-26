# Budget Tracker

A command line budget tracking tool built with Python.

## GUI Version (budget_tracker_gui.py)
- Full desktop interface built with Tkinter
- Color coded transaction rows — green for income, red for expenses
- Live summary bar showing income, expenses, and balance
- Spending by category — bar chart and pie chart
- Income vs expenses comparison chart
- Edit existing transactions
- Export to Excel with formatted headers and summary
- Export to CSV
- Dark mode toggle
- Data persists between sessions via JSON

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

## Roadmap
- ✅ Graphical User Interface (GUI) — Tkinter desktop app
- ✅ Export to Excel — openpyxl with formatted headers
- ✅ Export to CSV
- ✅ Data Persistence — JSON save and load
- ✅ Category Breakdown — matplotlib bar and pie charts
- **Dark mode polish** — full dark theme including frames and form areas
- **Date tracking** — add dates to transactions and filter by month
- **Budget limits** — set spending limits per category with warnings
- **Edit transaction** — ✅ completed
- **Monthly reports** — filter and summarize by month