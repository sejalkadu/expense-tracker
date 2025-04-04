import json
import os
from datetime import datetime
from collections import defaultdict

class ExpenseTracker:
    def __init__(self, data_file="expenses.json"):
        self.data_file = data_file
        self.expenses = []
        self.categories = {
            "1": "Food",
            "2": "Transportation",
            "3": "Entertainment",
            "4": "Housing",
            "5": "Utilities",
            "6": "Healthcare",
            "7": "Education",
            "8": "Other"
        }
        self.load_data()

    def load_data(self):
        """Load expense data from file if it exists"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    self.expenses = json.load(file)
            except (json.JSONDecodeError, IOError):
                print("Warning: Could not load expense data. Starting fresh.")
                self.expenses = []

    def save_data(self):
        """Save expense data to file"""
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.expenses, file, indent=4)
        except IOError:
            print("Error: Could not save expense data.")

    def get_valid_date(self, prompt):
        """Get a valid date input from user"""
        while True:
            date_str = input(prompt + " (YYYY-MM-DD or leave blank for today): ").strip()
            if not date_str:
                return datetime.now().strftime("%Y-%m-%d")
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

    def get_valid_amount(self, prompt):
        """Get a valid amount input from user"""
        while True:
            try:
                amount = float(input(prompt))
                if amount <= 0:
                    print("Amount must be positive. Please try again.")
                    continue
                return round(amount, 2)
            except ValueError:
                print("Invalid input. Please enter a number.")

    def add_expense(self):
        """Add a new expense to the tracker"""
        print("\n=== Add New Expense ===")
        
        amount = self.get_valid_amount("Enter amount spent: ")
        description = input("Enter a brief description: ").strip()
        date = self.get_valid_date("Enter expense date")
        
        print("\nAvailable Categories:")
        for num, category in self.categories.items():
            print(f"{num}. {category}")
        
        while True:
            category_choice = input("Select category number: ")
            if category_choice in self.categories:
                category = self.categories[category_choice]
                break
            print("Invalid category number. Please try again.")

        expense = {
            "date": date,
            "amount": amount,
            "description": description,
            "category": category
        }
        
        self.expenses.append(expense)
        self.save_data()
        print("\nExpense added successfully!")

    def edit_expense(self):
        """Edit an existing expense"""
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return
            
        self.view_expenses()
        
        try:
            idx = int(input("\nEnter expense number to edit: ")) - 1
            if 0 <= idx < len(self.expenses):
                expense = self.expenses[idx]
                print(f"\nEditing Expense {idx+1}:")
                print(f"1. Date: {expense['date']}")
                print(f"2. Amount: {expense['amount']}")
                print(f"3. Description: {expense['description']}")
                print(f"4. Category: {expense['category']}")
                
                field = input("\nEnter field number to edit (1-4) or 'cancel': ")
                
                if field == "1":
                    expense['date'] = self.get_valid_date("Enter new date")
                elif field == "2":
                    expense['amount'] = self.get_valid_amount("Enter new amount")
                elif field == "3":
                    expense['description'] = input("Enter new description: ").strip()
                elif field == "4":
                    print("\nAvailable Categories:")
                    for num, cat in self.categories.items():
                        print(f"{num}. {cat}")
                    new_cat = input("Enter new category number: ")
                    if new_cat in self.categories:
                        expense['category'] = self.categories[new_cat]
                elif field.lower() == 'cancel':
                    return
                
                self.save_data()
                print("\nExpense updated successfully!")
            else:
                print("Invalid expense number.")
        except ValueError:
            print("Please enter a valid number.")

    def delete_expense(self):
        """Delete an existing expense"""
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return
            
        self.view_expenses()
        
        try:
            idx = int(input("\nEnter expense number to delete: ")) - 1
            if 0 <= idx < len(self.expenses):
                confirm = input(f"Are you sure you want to delete expense {idx+1}? (y/n): ")
                if confirm.lower() == 'y':
                    del self.expenses[idx]
                    self.save_data()
                    print("\nExpense deleted successfully!")
            else:
                print("Invalid expense number.")
        except ValueError:
            print("Please enter a valid number.")

    def view_expenses(self, expenses=None):
        """View expenses (all or filtered)"""
        display_expenses = expenses if expenses else self.expenses
        
        if not display_expenses:
            print("\nNo expenses found.")
            return
            
        print(f"\n=== {'Filtered ' if expenses else ''}Expenses ===")
        for idx, expense in enumerate(display_expenses, 1):
            print(f"{idx}. Date: {expense['date']} | Amount: ${expense['amount']:.2f}")
            print(f"   Category: {expense['category']} | Description: {expense['description']}\n")

    def filter_expenses(self):
        """Filter expenses by date range or category"""
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return
            
        print("\n=== Filter Options ===")
        print("1. By date range")
        print("2. By category")
        print("3. Cancel")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            print("\nEnter start date:")
            start_date = self.get_valid_date("")
            print("\nEnter end date:")
            end_date = self.get_valid_date("")
            
            filtered = [e for e in self.expenses 
                       if start_date <= e['date'] <= end_date]
            self.view_expenses(filtered)
            
        elif choice == "2":
            print("\nAvailable Categories:")
            for num, category in self.categories.items():
                print(f"{num}. {category}")
            
            cat_choice = input("\nSelect category number: ")
            if cat_choice in self.categories:
                category = self.categories[cat_choice]
                filtered = [e for e in self.expenses 
                           if e['category'] == category]
                self.view_expenses(filtered)
            else:
                print("Invalid category selection.")

    def monthly_summary(self):
        """Show monthly summary of expenses"""
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return
            
        monthly_data = defaultdict(float)
        
        for expense in self.expenses:
            date = datetime.strptime(expense['date'], "%Y-%m-%d")
            month_year = date.strftime("%Y-%m")
            monthly_data[month_year] += expense['amount']
        
        print("\n=== Monthly Summary ===")
        for month, total in sorted(monthly_data.items()):
            print(f"{month}: ${total:.2f}")

    def category_summary(self):
        """Show category-wise expenditure with simple visualization"""
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return
            
        category_data = defaultdict(float)
        total = sum(expense['amount'] for expense in self.expenses)
        
        for expense in self.expenses:
            category_data[expense['category']] += expense['amount']
        
        print("\n=== Category-wise Expenditure ===")
        for category, amount in sorted(category_data.items(), 
                                     key=lambda x: x[1], reverse=True):
            percentage = (amount / total) * 100
            bar = '#' * int(percentage / 5)  # Each # represents 5%
            print(f"{category.ljust(15)}: ${amount:8.2f} {bar} ({percentage:.1f}%)")

    def run(self):
        """Main application loop"""
        while True:
            print("\n=== Expense Tracker ===")
            print("1. Add New Expense")
            print("2. View All Expenses")
            print("3. Edit Expense")
            print("4. Delete Expense")
            print("5. Filter Expenses")
            print("6. View Monthly Summary")
            print("7. View Category-wise Summary")
            print("8. Exit")
            
            choice = input("\nEnter your choice (1-8): ")
            
            actions = {
                "1": self.add_expense,
                "2": self.view_expenses,
                "3": self.edit_expense,
                "4": self.delete_expense,
                "5": self.filter_expenses,
                "6": self.monthly_summary,
                "7": self.category_summary,
                "8": lambda: print("\nThank you for using Expense Tracker!")
            }
            
            if choice in actions:
                actions[choice]()
                if choice == "8":
                    break
            else:
                print("\nInvalid choice. Please enter a number between 1-8.")

if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()