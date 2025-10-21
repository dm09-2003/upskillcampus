#!/usr/bin/env python3
"""
Personal Expense Tracker
A simple console-based application to track daily expenses
"""

import csv
import os
from datetime import datetime

# Global variables
EXPENSE_FILE = 'expenses.csv'
CATEGORIES = ['Food', 'Transport', 'Entertainment', 'Bills', 'Shopping', 'Health', 'Other']

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print application header"""
    print("=" * 60)
    print("           PERSONAL EXPENSE TRACKER")
    print("=" * 60)
    print()

def load_expenses():
    """Load expenses from CSV file"""
    expenses = []
    if os.path.exists(EXPENSE_FILE):
        try:
            with open(EXPENSE_FILE, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    expenses.append(row)
            print(f"✓ Loaded {len(expenses)} expenses from file.")
        except Exception as e:
            print(f"Error loading expenses: {e}")
    else:
        print("No existing expense file found. Starting fresh.")
    return expenses

def save_expenses(expenses):
    """Save expenses to CSV file"""
    try:
        with open(EXPENSE_FILE, 'w', newline='') as file:
            fieldnames = ['date', 'category', 'description', 'amount']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(expenses)
        print("✓ Expenses saved successfully!")
    except Exception as e:
        print(f"Error saving expenses: {e}")

def add_expense(expenses):
    """Add a new expense"""
    clear_screen()
    print_header()
    print("ADD NEW EXPENSE")
    print("-" * 60)

    # Get current date
    date = datetime.now().strftime('%Y-%m-%d')
    print(f"Date: {date}")

    # Show categories
    print("\nCategories:")
    for i, category in enumerate(CATEGORIES, 1):
        print(f"  {i}. {category}")

    # Get category
    while True:
        try:
            choice = int(input("\nSelect category (1-7): "))
            if 1 <= choice <= 7:
                category = CATEGORIES[choice - 1]
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Get description
    description = input("Description: ").strip()
    if not description:
        description = "No description"

    # Get amount
    while True:
        try:
            amount = float(input("Amount (₹): "))
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        except ValueError:
            print("Invalid amount. Please enter a number.")

    # Add expense
    expense = {
        'date': date,
        'category': category,
        'description': description,
        'amount': str(amount)
    }
    expenses.append(expense)

    print(f"\n✓ Expense added successfully!")
    print(f"  Category: {category}")
    print(f"  Description: {description}")
    print(f"  Amount: ₹{amount:.2f}")

    input("\nPress Enter to continue...")
    return expenses

def view_all_expenses(expenses):
    """View all expenses"""
    clear_screen()
    print_header()
    print("ALL EXPENSES")
    print("-" * 60)

    if not expenses:
        print("No expenses recorded yet.")
    else:
        print(f"{'#':<5} {'Date':<12} {'Category':<15} {'Description':<20} {'Amount':>10}")
        print("-" * 60)

        for i, expense in enumerate(expenses, 1):
            print(f"{i:<5} {expense['date']:<12} {expense['category']:<15} "
                  f"{expense['description'][:20]:<20} ₹{float(expense['amount']):>9.2f}")

        print("-" * 60)
        total = sum(float(e['amount']) for e in expenses)
        print(f"{'Total:':<52} ₹{total:>9.2f}")

    input("\nPress Enter to continue...")

def view_by_category(expenses):
    """View expenses by category"""
    clear_screen()
    print_header()
    print("EXPENSES BY CATEGORY")
    print("-" * 60)

    if not expenses:
        print("No expenses recorded yet.")
        input("\nPress Enter to continue...")
        return

    # Show categories with counts
    print("Categories:")
    for i, category in enumerate(CATEGORIES, 1):
        count = sum(1 for e in expenses if e['category'] == category)
        total = sum(float(e['amount']) for e in expenses if e['category'] == category)
        print(f"  {i}. {category:<15} ({count} expenses, ₹{total:.2f})")

    # Get category choice
    while True:
        try:
            choice = int(input("\nSelect category (1-7): "))
            if 1 <= choice <= 7:
                selected_category = CATEGORIES[choice - 1]
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Filter and display
    filtered = [e for e in expenses if e['category'] == selected_category]

    print(f"\n{selected_category.upper()} EXPENSES")
    print("-" * 60)

    if not filtered:
        print(f"No expenses in {selected_category} category.")
    else:
        print(f"{'#':<5} {'Date':<12} {'Description':<30} {'Amount':>10}")
        print("-" * 60)

        for i, expense in enumerate(filtered, 1):
            print(f"{i:<5} {expense['date']:<12} {expense['description'][:30]:<30} "
                  f"₹{float(expense['amount']):>9.2f}")

        print("-" * 60)
        total = sum(float(e['amount']) for e in filtered)
        print(f"{'Total:':<47} ₹{total:>9.2f}")

    input("\nPress Enter to continue...")

def view_summary(expenses):
    """View expense summary"""
    clear_screen()
    print_header()
    print("EXPENSE SUMMARY")
    print("-" * 60)

    if not expenses:
        print("No expenses recorded yet.")
    else:
        # Overall total
        total = sum(float(e['amount']) for e in expenses)
        print(f"Total Expenses: ₹{total:.2f}")
        print(f"Number of Transactions: {len(expenses)}")
        print(f"Average per Transaction: ₹{total/len(expenses):.2f}")

        print("\nCategory Breakdown:")
        print("-" * 60)
        print(f"{'Category':<20} {'Count':>8} {'Amount':>12} {'Percentage':>12}")
        print("-" * 60)

        for category in CATEGORIES:
            category_expenses = [e for e in expenses if e['category'] == category]
            if category_expenses:
                count = len(category_expenses)
                amount = sum(float(e['amount']) for e in category_expenses)
                percentage = (amount / total) * 100
                print(f"{category:<20} {count:>8} ₹{amount:>11.2f} {percentage:>11.1f}%")

        print("-" * 60)

    input("\nPress Enter to continue...")

def delete_expense(expenses):
    """Delete an expense"""
    clear_screen()
    print_header()
    print("DELETE EXPENSE")
    print("-" * 60)

    if not expenses:
        print("No expenses to delete.")
        input("\nPress Enter to continue...")
        return expenses

    # Show all expenses
    print(f"{'#':<5} {'Date':<12} {'Category':<15} {'Description':<20} {'Amount':>10}")
    print("-" * 60)

    for i, expense in enumerate(expenses, 1):
        print(f"{i:<5} {expense['date']:<12} {expense['category']:<15} "
              f"{expense['description'][:20]:<20} ₹{float(expense['amount']):>9.2f}")

    # Get expense to delete
    while True:
        try:
            choice = input(f"\nEnter expense number to delete (1-{len(expenses)}) or 'c' to cancel: ")
            if choice.lower() == 'c':
                return expenses

            choice = int(choice)
            if 1 <= choice <= len(expenses):
                deleted = expenses.pop(choice - 1)
                print(f"\n✓ Deleted expense: {deleted['description']} (₹{deleted['amount']})")
                break
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(expenses)}.")
        except ValueError:
            print("Invalid input. Please enter a number or 'c' to cancel.")

    input("\nPress Enter to continue...")
    return expenses

def main_menu():
    """Display main menu"""
    print_header()
    print("MAIN MENU")
    print("-" * 60)
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. View Expenses by Category")
    print("4. View Summary")
    print("5. Delete Expense")
    print("6. Save and Exit")
    print("-" * 60)

    choice = input("Enter your choice (1-6): ")
    return choice

def main():
    """Main application loop"""
    clear_screen()
    print_header()
    print("Welcome to Personal Expense Tracker!")
    print()

    # Load existing expenses
    expenses = load_expenses()
    input("\nPress Enter to continue...")

    # Main loop
    while True:
        clear_screen()
        choice = main_menu()

        if choice == '1':
            expenses = add_expense(expenses)
        elif choice == '2':
            view_all_expenses(expenses)
        elif choice == '3':
            view_by_category(expenses)
        elif choice == '4':
            view_summary(expenses)
        elif choice == '5':
            expenses = delete_expense(expenses)
        elif choice == '6':
            save_expenses(expenses)
            clear_screen()
            print_header()
            print("Thank you for using Personal Expense Tracker!")
            print("Your expenses have been saved.")
            print()
            break
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
