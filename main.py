from database import init_db, save_to_db,load_from_db,get_budgets,set_budget,update_expenses
from analytics import filter_category, filter_date, filter_amount,check_data_completeness,plot_category_pie, plot_daily_bar
import pandas as pd 
from datetime import datetime
init_db()
df = load_from_db()
def add_expences():
    try:
        amount_input = input("Enter the Amount: ").strip()
        if not amount_input:
            print("Error: Amount cannot be empty.")
            return
        amount = float(amount_input)
    except ValueError:
        print("Error: Invalid input! Please enter a numeric value (e.g., 10.50).")    
        return    
    category = input('Enter the category: ').strip()
    if not category:
        print("Error: Category cannot be empty.")
        return
    date_input = input('Enter the date (YYYY-MM-DD)[Leave blank for today]: ').strip()
    if not date_input:
        date = datetime.today().strftime('%Y-%m-%d')
    else:
        date = date_input
    try:
        save_to_db(amount, category , date)
        print("Expenses added Successfully")
        return load_from_db()
    except Exception as e:
        print(f"Error saving to database :{e}")
def show_summary(df):
        print('---all expences---')
        print(df)
        print('-------------')    
        print(f"Total expences is ${df['amount'].sum()}")    
        if not df.empty:
            budgets = get_budgets()
            category_total = df.groupby('category')['amount'].sum()
            print("\n--- Budget Alerts ---")
            alerts = False
            for category, total_spent in category_total.items():
                if category in budgets:
                    limit = budgets[category]
                    if total_spent > limit:
                        print(f"\033[1;31mWARNING: You are over budget for '{category}'! Spent: $ {total_spent} / Limit: ${limit}\033[0m")
                        alerts = True
            if not alerts :
                print("Great job! You are within your budget for all set categories.")
        print('--------------------\n')
def handel_edit_expenses(df):
    try:
        expenses_id = int(input("Enter the ID of the expenses to edit:").strip())
    except ValueError:
        print("Error : Invalid ID format. please enter a number.")
        return df 
    if expenses_id  not in df.index:
        print(f"Error : No expenses found with ID {expenses_id}.")
        return df 
    current_amount = df.loc[expenses_id,'amount']
    current_category = df.loc[expenses_id,'category']
    current_date = df.loc[expenses_id,'date'] 
    print(f"\n Editing Expenses {expenses_id} : {current_category} | ${current_amount} | {current_date}")
    print("(Press Enter without typing anything to keep the current value)")
    try:
        amount_input = input(f"Enter new amount [{current_amount}]:").strip()
        amount = float(amount_input) if amount_input else current_amount
    except ValueError:
        print("Error: Invalid amount entered. Edit cancelled. ")
        return df 
    
    category_input = input(f" Enter new category [{current_category}]:").strip()
    category = category_input if category_input else current_category

    date_input = input(f"Enter new date [{current_date}]:").strip()
    date = date_input if date_input else current_date

    update_expenses(expenses_id,amount,category,date)
    print("Expenses updated successfully!")
    return load_from_db()

def filter_choice(df):
    print("\n--- Filter Options ---")
    print("1: Filter by Category")
    print("2: Filter by Date")
    print('3: Filter by Amount')
    print('4: Check Data Completeness')
    choice = input('Enter your choice: ')
    
    if choice == '1':
        filter_category(df)
    elif choice == '2':
        filter_date(df)
    elif choice == '3':
        filter_amount(df)
    elif choice == '4':
        check_data_completeness(df)
    else:
        print('Invalid choice!!')
def handel_set_bedget():
    category = input('Enter the category for the budget :').strip()
    if not category:
        print("Error : Category cannot be empty.")
        return 
    try:
        limit_input = input(f"Enter the monthly limit for '{category}':").strip()
        limit = float(limit_input)
        set_budget(category,limit)
        print(f"Budget of $ {limit} set sucessfully for the '{category}' !")
    except ValueError:
        print("Error: Invalid input! Please enter a numeric value.")
def show_dashboard(df):
    print("\n---Dashboard---")
    print("1: Pie Chart (Spending by Category)")
    print("2: Bar Chart (Recent Daily Spending)")
    choice = input("Enter your choice:")
    if choice == '1':
        plot_category_pie(df)
    elif choice == '2':
        plot_daily_bar(df)
    else:
        print("Invalid Choice!")
while True :
    print("------------")
    print("1: Add expenses")
    print("2: Show expenses & Budget Summary")
    print("3: Filter type")
    print("4: Show dashboard")
    print("5: Set Category Budget") 
    print("6: Edit Expense")
    print("7: Exit")   

    selection=input("enter a choice:")

    if selection =='1':
        result=add_expences()
        if result is not None:
            df=result
    elif selection=='2':
        show_summary(df)
    elif selection=='3':
         filter_choice(df)
    elif selection=='4':
        show_dashboard(df)
    elif selection=='5':
        handel_set_bedget()
    elif selection=='6':
        df=handel_edit_expenses(df)
    elif selection =='7':
        print('exited')
        break    
    else:
        print("invalid choice!!")
       