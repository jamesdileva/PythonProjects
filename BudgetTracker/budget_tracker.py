# Budget Tracker
# A command line tool to track income and expenses

transactions = []

def add_transaction(type, category, amount, description):
    transaction = {
        "type": type,
        "category": category,
        "amount": amount,
        "description": description
    }
    transactions.append(transaction)
    print(f"\n✓ {type.capitalize()} of ${amount:.2f} added successfully.")

def get_valid_amount():
    while True:
        try:
            amount = float(input("Amount: $"))
            if amount <= 0:
                print("Amount must be greater than zero. Please try again.")
            else:
                return amount
        except ValueError:
            print("Invalid amount. Please enter a number.")

def get_valid_input(prompt):
    while True:
        value = input(prompt).strip()
        if len(value) >= 2 and any(c.isalpha() for c in value):
            return value
        print("Please enter a valid description using letters (at least 2 characters).")

def view_summary():
    if not transactions:
        print("\nNo transactions yet.")
        return
    
    income = sum(t["amount"] for t in transactions if t["type"] == "income")
    expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = income - expenses

    print("\n--- Budget Summary ---")
    print(f"Total Income:   ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Balance:        ${balance:.2f}")

def view_transactions():
    if not transactions:
        print("\nNo transactions yet.")
        return
    print("\n--- All Transactions ---")
    for i, t in enumerate(transactions, 1):
        print(f"{i}. [{t['type'].upper()}] {t['category']} - ${t['amount']:.2f} - {t['description']}")

def delete_transaction():
    if not transactions:
        print("\nNo transactions to delete.")
        return
    
    view_transactions()
    
    try:
        choice = int(input("\nEnter the number of the transaction to delete: "))
        if 1 <= choice <= len(transactions):
            removed = transactions.pop(choice - 1)
            print(f"\n✓ Transaction deleted: [{removed['type'].upper()}] {removed['category']} - ${removed['amount']:.2f}")
        else:
            print("\nInvalid number. Please try again.")
    except ValueError:
        print("\nPlease enter a valid number.")

def main():
    print("Welcome to Budget Tracker")
    while True:
        print("\nWhat would you like to do?")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. View All Transactions")
        print("5. Delete a Transaction")
        print("6. Exit")

        choice = input("\nEnter choice (1-6): ")

        if choice == "1":
            category = get_valid_input("Category (e.g. Salary, Freelance): ")
            amount = get_valid_amount()
            description = get_valid_input("Description: ")
            add_transaction("income", category, amount, description)

        elif choice == "2":
            category = get_valid_input("Category (e.g. Food, Rent, Transport): ")
            amount = get_valid_amount()
            description = get_valid_input("Description: ")
            add_transaction("expense", category, amount, description)

        elif choice == "3":
            view_summary()

        elif choice == "4":
            view_transactions()

        elif choice == "5":
            delete_transaction()

        elif choice == "6":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice. Please enter 1-6.")

main()