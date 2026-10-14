# Personal Expense Tracker — Python Mini Project

**Author:** Dharmesh Kumar  
**Language:** Python 3 | **Level:** Beginner  
**Storage:** CSV file; no external packages required.

A command-line app to record expenses, view saved records, calculate total spending, summarize spending by category, and delete incorrect entries. Data is saved locally in `data/expenses.csv`.

## Features
- Add expenses with date, category, description, and amount
- Use today's date automatically or enter `YYYY-MM-DD`
- View all records and total spending
- Show spending totals and percentages by category
- Delete an expense by its displayed number
- Validate dates and amounts

## Run in VS Code
1. Install Python 3.8 or newer.
2. Open this folder in VS Code.
3. Choose **Terminal → New Terminal**.
4. Run `python expense_tracker.py` (or `python3 expense_tracker.py`).
5. Choose a menu option. Data is stored in `data/expenses.csv`.

## Project Structure
```text
Python_Personal_Expense_Tracker/
├── expense_tracker.py
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── data/
│   └── .gitkeep
└── tests/
    └── test_expense_tracker.py
```

## Concepts Practiced
Functions, loops, conditional statements, lists, dictionaries, CSV file handling, date validation, exception handling, sorting, and aggregation.

## Future Improvements
Monthly budgets, charts with Matplotlib, monthly reports, a Tkinter GUI, or SQLite storage.

## License
MIT License. See `LICENSE`.
