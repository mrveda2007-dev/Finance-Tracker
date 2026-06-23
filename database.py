import sqlite3
import hashlib
from sqlalchemy.engine import cursor
import hashlib
import pandas as pd
import sqlite3
def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor =  conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            date TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets(
            category TEXT UNIQUE,
            monthly_limit REAL 
        )
    ''')
    conn.commit()
    conn.close()
def save_to_db(amount , category ,date,user_id = None):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (amount,category,date,user_id) VALUES (?,?,?,?)""",
        (amount, category ,date,user_id)
    )    
    conn.commit()
    conn.close()
def load_from_db(user_id=None):
    conn = sqlite3.connect("expenses.db")
    if user_id:
        df = pd.read_sql_query("SELECT * FROM expenses WHERE user_id = ?",conn,params=(user_id,),index_col="id")
    else:
        df = pd.read_sql_query("SELECT * FROM expenses",conn,index_col="id")
    conn.close()
    return df
def set_budget(category, limit,user_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM budgets WHERE category = ? AND user_id =?",(category,user_id))
    cursor.execute("""
        INSERT OR REPLACE INTO budgets (category , monthly_limit) VALUES (?,?)""",
        (category , limit ))
    conn.commit()
    conn.close()
def get_budgets(user_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute(" SELECT category ,monthly_limit FROM budgets WHERE user_id = ?",(user_id,))
    budgets = {row[0] : row[1] for row in cursor.fetchall()}
    conn.close()
    return budgets
def update_expenses(expenses_id,amount,category,date,user_id):
    conn=sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE expenses 
        SET amount = ?, category = ? ,date = ? 
        WHERE id = ? AND user_id = ?
    ''' ,(amount,category,date,int(expenses_id),int(user_id))
    )
    conn.commit()
    conn.close()
def init_users_table():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
            )
    ''')
    try:
        cursor.execute("ALTER TABLE expenses ADD COLUMN user_id INTEGER")
    except:
        pass 
    try:
        cursor.execute("ALTER TABLE budgets ADD COLUMN user_id INTEGER")
    except:
        pass 
    conn.commit()
    conn.close()
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
def register_user(name,email,password):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id,name FROM users WHERE email = ?",(email,))
    
    if cursor.fetchone():
        conn.close()
        return None
    hashed = hash_password(password)
    cursor.execute(
        "INSERT INTO users (name, email , password) VALUES (?,?,?)",
        (name,email,hashed)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id
def login_user(email,password):
    conn =sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute("SELECT id, name FROM users WHERE email =? AND password =?",
        (email,hashed)
    )
    user = cursor.fetchone()
    conn.close()
    if user :
        return user[0],user[1]
    return None
def delete_expenses(expenses_id , user_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM expenses
        WHERE id =? AND user_id = ?
    
    ''',(int(expenses_id),int(user_id)))
    conn.commit()
    conn.close()


    