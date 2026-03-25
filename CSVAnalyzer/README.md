# CSV Data Analyzer

A command line tool to analyze CSV financial data and produce summary reports.

## Features
- Load and validate CSV files
- Financial summary — total income, expenses, and balance
- Category breakdown — spending grouped by category
- Expense statistics — highest, lowest, and average
- Export report to a text file
- Data cleaning — handles missing, invalid, and negative values

## How to Run
Install dependencies:
```
pip install pandas
```
Then run:
```
python csv_analyzer.py
```

## Usage
1. View Financial Summary — total income, expenses, and balance
2. View Category Breakdown — expenses grouped by category
3. View Expense Statistics — highest, lowest, and average expense
4. Export Report to File — saves a report.txt summary
5. Exit

## Roadmap
- **Multiple file support** — let the user choose which CSV to analyze
- **Date range filtering** — analyze a specific month or week
- **Category filtering** — drill down into a single category
- **Visual charts** — bar chart of spending by category using matplotlib
- **Excel export** — export report to .xlsx using openpyxl
- **Top 5 transactions** — show the largest expenses
- **Month over month comparison** — compare two CSV files
```
