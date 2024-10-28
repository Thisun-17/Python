import json
import datetime


# Validate the provided date against the current date and format constraints.
def validate_date(date_text):
    try:
        # Attempt to parse the input date and compare it to today's date.
        input_date = datetime.datetime.strptime(date_text, '%Y-%m-%d').date()
        current_date = datetime.date.today()
        if input_date > current_date:
            # Future dates are not allowed.
            return False, "Date cannot be in the future."
        return True, ""
    except ValueError:
        # Handle cases where the date format is incorrect.
        return False, "Invalid date or format. Please enter the date in (YYYY-MM-DD) format."


# Load transactions from a JSON file, handling errors for file not found or JSON decode errors.
def load_transactions():
    global transactions
    
    try:
        with open('transactions.json', 'r') as file:
            transactions = json.load(file)
    except FileNotFoundError:
        # File doesn't exist; start with an empty list and notify the user.
        print("Transactions file not found. A new file will be created.")
        transactions = []
    except json.JSONDecodeError:
        # JSON file is corrupt; start with an empty list and notify the user.
        print("Error reading transactions file. Starting with an empty list.")
        transactions = []


# Save the current state of transactions to a JSON file.
def save_transactions():
    with open('transactions.json', 'w') as file:
        json.dump(transactions, file)


# Add a new transaction after validating the user input for amount, category, type, and date.
def add_transaction():
    while True:
        input_str = input("Enter the transaction amount: ").strip()
        if not input_str:
            print("Amount cannot be empty.")
            continue
        try:
            amount = float(input_str)
            if amount <= 0:
                print("Amount must be greater than 0. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a numerical value.")
            
    while True:
        category = input("Enter the transaction category: ").strip()
        if not category:
            print("Category cannot be empty.")
            continue
        if category.isalpha():
            break
        else:
            print("Category name must consist of alphabetic characters only.")

    while True:
        transaction_type = input("Enter the transaction type (Income/Expense): ").lower().strip()
        if not transaction_type:
            print("Transaction type cannot be empty.")
            continue
        if transaction_type in ['income', 'expense']:
            break
        else:
            print("Invalid transaction type. Please enter 'Income' or 'Expense'.")

    while True:
        date = input("Please enter the transaction date in the format (YYYY-MM-DD): ").strip()
        if not date :
            print("Date cannot be empty.")
        is_valid, message = validate_date(date)
        if not is_valid:
            print(message)  # Print the error message returned from validate_date
            continue
        break  # If is_valid is True, break out of the loop

    # Construct and append the new transaction.
    Transaction = [amount, category, transaction_type, date]
    transactions.append(Transaction)
    save_transactions()
    print("Transaction added successfully.")

# Display all transactions to the user.
def view_transactions():
    if not transactions :
        print("No transactions available to view.")
    for index, transaction in enumerate(transactions):
        print(f"{index+1}: Amount: {transaction[0]}, Category: {transaction[1]}, Type: {transaction[2]}, Date: {transaction[3]}")

# Update an existing transaction selected by the user.
def update_transaction():
    if not transactions:
        print("No transactions available to update.")
        return
    view_transactions()

    while True:
        choice_input = input("Enter the number of the transaction you want to update (or '0' to cancel): ").strip()
        if not choice_input:
            print("Input cannot be empty.")
            continue

        try:
            choice = int(choice_input) - 1  # Adjust for zero-based index of the list
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == -1:
            print("Transaction update canceled.")
            return
        elif 0 <= choice < len(transactions):
            break
        else:
            print(f"Invalid transaction number. Please enter a number between 1 and {len(transactions)}, or '0' to cancel.")

    while True:
        input_str = input("Enter the transaction amount: ").strip()
        if not input_str:
            print("Amount cannot be empty.")
            continue
        try:
            amount = float(input_str)
            if amount <= 0:
                print("Amount must be greater than 0. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a numerical value.")

    while True:
        category = input("Enter the transaction category: ").strip()
        if not category:
            print("Category cannot be empty.")
            continue
        if category.isalpha():
            break
        else:
            print("Invalid category. Please use only letters.")

    while True:
        transaction_type = input("Enter the transaction type (Income/Expense): ").lower().strip()
        if not transaction_type:
            print("Transaction type cannot be empty.")
            continue
        if transaction_type in ['income', 'expense']:
            break
        else:
            print("Invalid transaction type. Please enter 'Income' or 'Expense'.")

    while True:
        date = input("Please enter the new transaction date (YYYY-MM-DD): ").strip()
        if not date :
            print("Date cannot be empty.")
        is_valid, message = validate_date(date)
        if not is_valid:
            print(message)  # Inform the user why the date is invalid
            continue
        break

    # Update the selected transaction with new details.
    transactions[choice] = [amount, category, transaction_type, date]
    save_transactions()
    print("Transaction updated successfully.")

# Delete a specified transaction after confirmation from the user.
def delete_transaction():
    if not transactions:
        print("No transactions available to delete.")
        return

    view_transactions()
    print("Please enter the number of the transaction you want to delete, (or enter '0' to cancel.) ")

    while True:
        choice_input = input("Choice: ").strip()
        if not choice_input:
            print("Choice cannot be empty.")
            continue

        try:
            choice = int(choice_input) - 1  # Adjust for zero-based index of the list
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        if choice == -1:
            print("Transaction deletion canceled.")
            return
        elif 0 <= choice < len(transactions):
            break
        else:
            print(f"Invalid transaction number. Please enter a number between 1 and {len(transactions)}, or '0' to cancel.")
    
    # Proceed to delete the transaction
    del transactions[choice]
    save_transactions()
    print("Transaction deleted successfully.")

# Display a summary of income, expense, and the balance.
def display_summary():
    total_income = sum(transaction[0] for transaction in transactions if transaction[2] == "income")
    total_expense = sum(transaction[0] for transaction in transactions if transaction[2] == "expense")

    balance = total_income - total_expense
    print(f"Total Income: {total_income}")
    print(f"Total Expense: {total_expense}")
    print(f"Balance: {balance}")

# Main menu loop, providing options to the user for managing their transactions.
def main_menu():
    load_transactions()

    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        if not choice:
            print("Choice cannot be empty")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
             update_transaction()
        elif choice == '4':
             delete_transaction()
        elif choice == '5':
             display_summary()
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
