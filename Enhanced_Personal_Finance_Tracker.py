import json
import datetime
import tkinter as tk
from tkinter import ttk

# Global dictionary to store transactions
transactions = {}

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

def load_transactions():
    #Load transaction data from a JSON file.
    global transactions
    try:
        with open('transactions.json', 'r') as file:
            transactions = json.load(file)
    except FileNotFoundError:
        transactions = {}

def save_transactions():
    #Save the current transactions to a JSON file.
    with open('transactions.json', 'w') as file:
        json.dump(transactions, file, indent=4)

def add_transaction():
    #Add a new transaction after collecting input from the user.
    while True: 
        transaction_type = input("Enter the transaction type (Income/Expense): ").lower().strip()
        if not transaction_type:
            print("Transaction type cannot be empty.")
            continue
        if transaction_type not in ['income', 'expense']:
            print("Invalid transaction type. Please enter 'Income' or 'Expense'.")
            continue
        break

    while True:
        category = input("Enter the transaction category: ").lower().strip()
        if not category:
            print("Category cannot be empty.")
            continue
        if not category.isalpha():
            print("Category name must consist of alphabetic characters only.")
            continue
        break

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
        date = input("Please enter the transaction date in the format (YYYY-MM-DD): ").strip()
        if not date:
            print("Date cannot be empty.")
            continue
        is_valid, message = validate_date(date)
        if not is_valid:
            print(message)  # Print the error message returned from validate_date
            continue
        break  # If is_valid is True, break out of the loop

    # Initialize the transaction_type key if it doesn't exist
    if transaction_type not in transactions:
        transactions[transaction_type] = {}
    if category not in transactions[transaction_type]:
        transactions[transaction_type][category] = []

    transaction = {"amount": amount, "date": date}
    transactions[transaction_type][category].append(transaction)

    save_transactions()
    print("Transaction added successfully.")


def view_transactions():
    #Display all stored transactions.
    if not transactions:
        print("No transactions available to view.")
        return
    for transaction_type, categories in transactions.items():
        print(f"Transaction type: {transaction_type.capitalize()}")
        if isinstance(categories, dict):  # Check if categories is a dictionary
            for category, transaction_list in categories.items():
                print(f"\tCategory: {category}")
                for transaction in transaction_list:
                    print(f"\t\tAmount: {transaction['amount']}, Date: {transaction['date']}")
        elif isinstance(categories, list):  # Check if categories is a list
            for transaction in categories:
                print(f"\tAmount: {transaction['amount']}, Date: {transaction['date']}")

def delete_transaction():
    #Allow the user to delete a transaction.
    if not transactions:
        print("No transactions available to delete.")
        return
    
    view_transactions()
    
    while True:
        transaction_type = input("Enter the transaction type of the transaction you want to delete: ").lower().strip()
        
        if not transaction_type:
            print("Transaction type cannot be empty.")
            continue
        
        if transaction_type not in transactions:
            print("Transaction type does not exist.")
            continue
        
        if not transaction_type.isalpha():
            print("Transaction type must consist of alphabetic characters only.")
            continue
        break
    while True:
    
        category = input("Enter the category of the transaction you want to delete: ").lower().strip()
        if not category:
            print("Category cannot be empty.")
            continue 
        if category not in transactions[transaction_type]:
            print("Category does not exist.")
            continue 
        if not category.isalpha():
            print("Invalid category. Please use only letters.")
            continue
        break 

        # Print the transactions in the selected category for debugging
        
    list_transactions_in_category(transaction_type, category)

   
    while True:
        input_str = input("Enter the index of the transaction you want to delete: ").strip()
        if not input_str:
            print("Transaction index cannot be empty.")
            continue 
        try:
            transaction_index = int(input_str)
            if transaction_index < 0 or transaction_index >= len(transactions[transaction_type][category]):
                print("Invalid transaction index.")
                continue 
        except ValueError:
            print("Invalid index. Please enter a numerical value.")
            continue
        break 

    del transactions[transaction_type][category][transaction_index]
    try:
        if not transactions[transaction_type][category]:
            del transactions[transaction_type][category]
    
                
        if not transactions[transaction_type]:
            del transactions[transaction_type]

        save_transactions()
        print("Transaction deleted successfully.")
        return  # Exit the function after successful deletion
    except ValueError:
        print("Please enter a valid index.")
    

def list_transactions_in_category(transaction_type, category):
    print(f"Transactions in '{category}' under '{transaction_type.capitalize()}':")
    for i, transaction in enumerate(transactions[transaction_type][category]):
        print(f"{i}. Amount: {transaction['amount']}, Date: {transaction['date']}")


def update_transaction():
    #Allow the user to update details of a specific transaction.
    if not transactions:
        print("No transactions available to update.")
        return
    view_transactions()
    while True:
    
        transaction_type = input("Enter the type of the transaction you want to update (Income/Expense): ").lower().strip()
        if not transaction_type:
            print("Transaction type cannot be empty.")
            continue 
        if transaction_type not in transactions:
            print("Transaction type does not exist.")
            continue 
        if not transaction_type.isalpha():
            print("Invalid transaction type. Please use only letters.")
        break

    while True:
    
        category = input("Enter the category of the transaction you want to update: ").lower().strip()
        if not category:
            print("Category cannot be empty.")
            continue 
        if category not in transactions[transaction_type]:
            print("Category does not exist.")
            continue 
        if not category.isalpha():
            print("Invalid category. Please use only letters.")
            continue
        break 
    
    list_transactions_in_category(transaction_type, category)
    while True:
        input_str = input("Enter the index of the transaction you want to update: ").strip()
        if not input_str:
            print("Transaction index cannot be empty.")
            continue
        
        try:
            transaction_index = int(input_str)
            if transaction_index < 0 or transaction_index >= len(transactions[transaction_type][category]):
                print("Invalid transaction index.")
                continue
        except ValueError:
            print("Invalid index. Please enter a numerical value.")
            continue

        break  # If all checks pass, break out of the loop

    while True:
        new_transaction_type = input("Enter the new transaction type (Income/Expense): ").lower().strip()
        if not transaction_type:
            print("Transaction type cannot be empty.")
            continue
        if new_transaction_type in ['income', 'expense']:
            break
        else:
            print("Invalid transaction type. Please enter 'Income' or 'Expense'.")

    while True:  
        new_category = input("Enter the transaction new category: ").lower().strip()
        if not new_category:
            print("Category cannot be empty.")
            continue
        if not new_category.isalpha():
            print("Category name must consist of alphabetic characters only.")
            continue
        break
   
    while True:
        input_str = input("Enter the transaction new amount: ").strip()
        if not input_str:
            print("Amount cannot be empty.")
            continue 
        try:
            amount = float(input_str)
            if amount <= 0:
                print("Amount must be greater than 0. Please try again.")
                continue 
        except ValueError:
            print("Invalid amount. Please enter a numerical value.")
            continue
        break

    while True:
        date = input("Please enter the new transaction date (YYYY-MM-DD): ").strip()
        if not date:
            print("Date cannot be empty.")
            continue 
        is_valid, message = validate_date(date)
        if not is_valid:
            print(message)  # Inform the user why the date is invalid
            continue
        break

     # If all inputs are valid, perform the update
    if new_transaction_type and new_category and amount and date:
        # Move the transaction to the new category/type if necessary
        transaction = transactions[transaction_type][category].pop(transaction_index)
        if not transactions[transaction_type][category]:
            del transactions[transaction_type][category]

        # Add the transaction to the new type/category
        if new_category not in transactions[new_transaction_type]:
            transactions[new_transaction_type][new_category] = []
        transactions[new_transaction_type][new_category].append({
            "amount": amount,
            "date": date
        })

    # If all validations pass, then update the transaction
    
    print("Transaction updated successfully.")


def total_summary():
    #Calculate and display total income, expenses, and net total.
    if not transactions:
        print("No transactions available.")
        return

    total_income = 0
    total_expense = 0

    for transaction_type, categories in transactions.items():
        for category, transactions_list in categories.items():
            for transaction in transactions_list:
                amount = transaction['amount']
                if transaction_type == 'income':
                    total_income += amount
                elif transaction_type == 'expense':
                    total_expense += amount

    print("Total Income:", total_income)
    print("Total Expense:", total_expense)
    print("Net Total:", total_income - total_expense)
# The main transactions dictionary to store all data
transactions = {}

def read_bulk_transactions_from_file(filename):
    global transactions  # Ensure we are modifying the global dictionary
    added_transactions = {}

    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) != 4:
                    print("Skipping invalid entry:", line)
                    continue

                transaction_type, category, amount, date = parts
                amount = float(amount)

                if transaction_type not in added_transactions:
                    added_transactions[transaction_type] = {}
                if category not in added_transactions[transaction_type]:
                    added_transactions[transaction_type][category] = []

                transaction = {"amount": amount, "date": date}
                added_transactions[transaction_type][category].append(transaction)

                if transaction_type not in transactions:
                    transactions[transaction_type] = {}
                if category not in transactions[transaction_type]:
                    transactions[transaction_type][category] = []
                transactions[transaction_type][category].append(transaction)

        print("Bulk transactions read and displayed below:")
        display_transactions(added_transactions)
        print("Now saving transactions...")
        save_transactions()  # Ensure this is called to save changes
    except FileNotFoundError:
        print("File not found.")
    except ValueError:
        print("Error processing a line. Check file format.")
    except Exception as e:
        print(f"An error occurred: {e}")


def display_transactions(transactions):
    if not transactions:
        print("No transactions available to display.")
        return
    
    for transaction_type, categories in transactions.items():
        print(f"\nTransaction type: {transaction_type.capitalize()}")
        for category, transaction_list in categories.items():
            print(f"  Category: {category.capitalize()}")
            for transaction in transaction_list:
                print(f"    Amount: {transaction['amount']}, Date: {transaction['date']}")


class FinanceTrackerApp:
        def __init__(self, root):
            self.root = root
            self.root.title('Enhanced Personal Finance Tracker')
            self.root.geometry('800x600')

            self.data = self.load_data("transactions.json")
            self.create_widgets()
            self.display_data()

        def create_widgets(self):
            # Treeview for displaying transactions
            self.tree = ttk.Treeview(self.root, columns=("Date", "Type", "Category", "Amount"), show='headings')
            self.tree.heading("Date", text="Date", command=lambda: self.treeview_sort_column("Date", False))
            self.tree.heading("Type", text="Type", command=lambda: self.treeview_sort_column("Type", False))
            self.tree.heading("Category", text="Category", command=lambda: self.treeview_sort_column("Category", False))
            self.tree.heading("Amount", text="Amount", command=lambda: self.treeview_sort_column("Amount", False))
            self.tree.pack(fill=tk.BOTH, expand=True)

            # Search fields and button
            self.search_frame = tk.Frame(self.root)
            self.search_frame.pack(pady=20)

            tk.Label(self.search_frame, text="Date (YYYY-MM-DD):").pack(side=tk.LEFT, padx=6)
            self.search_date_var = tk.StringVar()
            self.search_date_entry = ttk.Entry(self.search_frame, textvariable=self.search_date_var)
            self.search_date_entry.pack(side=tk.LEFT, padx=6)

            tk.Label(self.search_frame, text="Type (Income/Expense):").pack(side=tk.LEFT, padx=6)
            self.search_type_var = tk.StringVar()
            self.search_type_entry = ttk.Entry(self.search_frame, textvariable=self.search_type_var)
            self.search_type_entry.pack(side=tk.LEFT, padx=6)

            tk.Label(self.search_frame, text="Amount:").pack(side=tk.LEFT, padx=6)
            self.search_amount_var = tk.StringVar()
            self.search_amount_entry = ttk.Entry(self.search_frame, textvariable=self.search_amount_var)
            self.search_amount_entry.pack(side=tk.LEFT, padx=6)

            self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search_transactions)
            self.search_button.pack(side=tk.LEFT, padx=6)

            self.reset_button = ttk.Button(self.search_frame, text="Reset", command=self.reset_search)
            self.reset_button.pack(side=tk.LEFT, padx=6)

        def display_data(self, data=None):
            if data is None:
                data = self.data
            self.tree.delete(*self.tree.get_children())
            for transaction_type, categories in data.items():
                for category, transactions in categories.items():
                    for transaction in transactions:
                        # Assuming transaction is a dictionary with 'date' and 'amount'
                        if all(key in transaction for key in ['date', 'amount']):
                            self.tree.insert('', 'end', values=(
                                transaction["date"],
                                transaction_type.capitalize(),
                                category.capitalize(),
                                transaction["amount"]
                            ))

        def load_data(self, filepath):
            try:
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    # Ensure that the data is a dictionary
                    if isinstance(data, dict):
                        self.data = data
                        return data
                    else:
                        raise ValueError("Data loaded is not a dictionary.")
            except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
                print(f"Error loading data: {e}")
                self.data = {} 
                return {}  # Return an empty dictionary on error
            except Exception as e:
                print(f"Unexpected error: {e}")
                self.data = {}
                return {}
            
        def search_transactions(self):
            search_date = self.search_date_var.get().strip()
            search_type = self.search_type_var.get().strip().lower()
            search_amount = self.search_amount_var.get().strip()

            filtered_data = {}
            for t_type, categories in self.data.items():
                if search_type and t_type.lower() != search_type:
                    continue
                filtered_categories = {}
                for category, transactions in categories.items():
                    filtered_transactions = [
                        transaction for transaction in transactions
                        if (search_date == "" or transaction["date"] == search_date) and
                           (search_amount == "" or str(transaction["amount"]) == search_amount)
                    ]
                    if filtered_transactions:
                        filtered_categories[category] = filtered_transactions
                if filtered_categories:
                    filtered_data[t_type] = filtered_categories

            self.display_data(filtered_data)

       
        def reset_search(self):
            # Reset the search fields
            self.search_date_var.set("")
            self.search_type_var.set("")
            self.search_amount_var.set("")

            # After resetting the fields, display all transactions again
            self.display_data()  # Call display_data without arguments to use self.data


        def treeview_sort_column(self, col, reverse):
            l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
            if col == "Amount":
                l.sort(key=lambda t: float(t[0]), reverse=reverse)
            else:
                l.sort(reverse=reverse)
            for index, (val, k) in enumerate(l):
                self.tree.move(k, '', index)
            self.tree.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))


def launch_gui():
    root = tk.Tk()
    app = FinanceTrackerApp(root)
    root.mainloop()



def main_menu():
    #Handle the main menu interactions for the finance tracker.
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Total Summary")
        print("6. Read Bulk Transactions From File")
        print("7. Launch the GUI")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()
        if not choice:
            print("Choice cannot be empty")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            update_transaction()
        elif choice == "4":
            delete_transaction()
        elif choice== "5":
            total_summary()
        elif choice == "6":
            filename = input("Enter filename: ")
            read_bulk_transactions_from_file(filename)
        elif choice == "7":
            launch_gui()
        elif choice == "0":
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    load_transactions()
    main_menu()
