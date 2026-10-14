"""Personal Expense Tracker | Author: Dharmesh Kumar"""
import csv
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]


def ensure_data_file():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        with DATA_FILE.open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()


def read_expenses():
    ensure_data_file()
    with DATA_FILE.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def add_expense():
    print("\n--- Add an Expense ---")
    date_text = input("Date (YYYY-MM-DD, blank for today): ").strip()
    if not date_text:
        date_text = datetime.today().strftime("%Y-%m-%d")
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    category = input("Category (Food, Travel, Bills, Shopping, Other): ").strip().title()
    if not category:
        print("Category cannot be empty.")
        return
    description = input("Description: ").strip()
    try:
        amount = float(input("Amount: ").strip())
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Amount must be a number greater than zero.")
        return

    ensure_data_file()
    with DATA_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow({
            "date": date_text, "category": category,
            "description": description, "amount": f"{amount:.2f}"
        })
    print("Expense saved successfully!")


def show_expenses():
    expenses = read_expenses()
    print("\n--- All Expenses ---")
    if not expenses:
        print("No expenses recorded yet.")
        return
    print(f"{'No.':<5}{'Date':<13}{'Category':<16}{'Amount':>12}  Description")
    print("-" * 75)
    for i, e in enumerate(expenses, 1):
        print(f"{i:<5}{e['date']:<13}{e['category']:<16}{float(e['amount']):>12.2f}  {e['description']}")
    print("-" * 75)
    print(f"Total spent: {sum(float(e['amount']) for e in expenses):.2f}")


def show_summary():
    expenses = read_expenses()
    print("\n--- Expense Summary ---")
    if not expenses:
        print("No expenses available to summarize.")
        return
    total = sum(float(e["amount"]) for e in expenses)
    categories = {}
    for e in expenses:
        categories[e["category"]] = categories.get(e["category"], 0) + float(e["amount"])
    print(f"Number of expenses: {len(expenses)}")
    print(f"Total spending: {total:.2f}")
    print("\nSpending by category:")
    for category, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category:<18} {amount:>10.2f} ({amount / total * 100:.1f}%)")


def delete_expense():
    expenses = read_expenses()
    if not expenses:
        print("There are no expenses to delete.")
        return
    show_expenses()
    choice = input("Expense number to delete (Enter to cancel): ").strip()
    if not choice:
        print("Delete cancelled.")
        return
    try:
        index = int(choice)
        if not 1 <= index <= len(expenses):
            raise ValueError
    except ValueError:
        print("Enter a valid expense number.")
        return
    removed = expenses.pop(index - 1)
    with DATA_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expenses)
    print(f"Deleted: {removed['description'] or removed['category']}")


def main():
    ensure_data_file()
    while True:
        print("\n" + "=" * 42)
        print("       PERSONAL EXPENSE TRACKER")
        print("=" * 42)
        print("1. Add expense\n2. View all expenses\n3. View spending summary\n4. Delete an expense\n5. Exit")
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            print("Your expenses are saved. Goodbye!")
            break
        else:
            print("Invalid option. Choose from 1 to 5.")


if __name__ == "__main__":
    main()
