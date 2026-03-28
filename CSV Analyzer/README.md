# CSV Analyzer

A desktop data analysis tool that loads any CSV file and produces
financial summaries, category breakdowns, and visual charts.

## Version History

### v1.1 — CustomTkinter Modern UI
- Complete UI rebuild using CustomTkinter
- Slate and amber color scheme — analyst tool aesthetic
- Always-visible right stats panel — no tab switching needed
- Summary, top categories, and statistics visible simultaneously
- Inline category filter in the toolbar
- Themed matplotlib charts — slate dark background
- Improved dark mode with scrollable stats panel

### v1.0 — Original GUI
- Tkinter desktop app with tabbed layout
- Category filter, top 5 expenses tab, statistics tab
- Charts, dark mode, Excel and report export

## How to Run

**download the executable** from the
[Releases](https://github.com/jamesdileva/Python-Projects/releases/tag/csv-analyzer-v1.1)
page — no Python installation required. Windows only.

**GUI version:**
```
python csv_analyzer_gui.py
```

**Command line version:**
```
python csv_analyzer.py
```

## Dependencies
```
pip install pandas matplotlib openpyxl
```


## Features

### v1.0 — Original GUI
- Tkinter desktop app with tabbed layout
- Category filter, top 5 expenses tab, statistics tab
- Charts, dark mode, Excel and report export
- Browse and load any CSV file from your computer
- Live summary bar — total income, expenses, and balance
- Four analysis tabs:
  - All Transactions — full data table with color coded rows
  - Category Breakdown — total spent, transaction count, and average per category
  - Top 5 Expenses — the five largest expense transactions
  - Statistics — highest, lowest, average, and median expense
- Filter transactions by category with a dropdown
- Spending by category — bar chart and pie chart
- Income vs expenses comparison chart with surplus/deficit indicator
- Export summary report to text file
- Export all transactions to formatted Excel file
- Dark mode toggle
- Handles missing, invalid, and negative values automatically

### Command Line Version
- Load and validate CSV files
- Financial summary — total income, expenses, and balance
- Category breakdown — spending grouped by category
- Expense statistics — highest, lowest, and average
- Export report to text file
- Data cleaning — handles missing, invalid, and negative values

## CSV Format
The analyzer expects a CSV file with these columns:
```
date, category, description, amount, type
```
Where type is either `income` or `expense`.

## Roadmap

### Completed
- ✅ GUI — Tkinter desktop app
- ✅ Filter by category — dropdown filter on transaction table
- ✅ Top 5 largest expenses — dedicated tab
- ✅ Multiple CSV file support — browse for any CSV file
- ✅ Export to Excel — formatted with colored headers
- ✅ Export report to text file
- ✅ Dark mode toggle
- ✅ Data cleaning — invalid and negative value handling

### Planned
- **Date range filtering** — analyze a specific month or week
- **Month over month comparison** — load and compare two CSV files
- **Visual charts in window** — embed charts directly in the app tabs
- **Dark mode polish** — full theme coverage including all frames
- **Custom column mapping** — support CSV files with different column names
- **Database export** — save analyzed data to SQLite
