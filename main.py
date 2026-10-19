import streamlit as st
import plotly as pt
import pandas as pd
import sqlite3 as sql
from datetime import datetime as dt

def init_db():
    conn = sql.connect("expenses.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            product TEXT,
            price REAL,
            note TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS settings(
            key TEXT PRIMARY KEY,
            value REAL
        )
    ''')
    
    conn.commit()
    conn.close()

def get_monthly_budget():
    conn = sql.connect("expenses.db")
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key = 'monthly_budget'")
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0.0

def set_monthly_budget(amount):
    conn = sql.connect("expenses.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO settings (key, value) VALUES ('monthly_budget', ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value
    """,
        (amount,),
    )
    
    conn.commit()
    conn.close()
    

def add_expense(date, product, price, note):
    conn = sql.connect("expenses.db")
    c = conn.cursor()
    date_str = date.strftime("%Y-%m-%d")
    c.execute('''
        INSERT INTO expenses(date, product, price, note)
        VALUES (?, ?, ?, ?)
    ''', (date_str, product, price, note))
    conn.commit()
    conn.close()

def get_total_expenses():
    conn = sql.connect("expenses.db")
    c = conn.cursor()
    c.execute("SELECT SUM(price) FROM expenses")
    row = c.fetchone()
    conn.close()
    return row[0] if row and row[0] else 0.0

init_db()


st.title("Expense Tracker")

saved_budget = get_monthly_budget()

monthly_expense = st.number_input(
    label="Monthly Budget",
    value=float(saved_budget),
    placeholder="Enter your monthly expense limit."
)

if monthly_expense != saved_budget:
    set_monthly_budget(monthly_expense)
    st.toast("Updated Monthly Budget!")

st.divider()

date = st.date_input(label="Date", value="today")
product = st.text_input(label="Product Name", placeholder="Enter Product Name")
price = st.number_input(label="Price", placeholder="Enter price of the product")
note = st.text_input(label="Note", placeholder="Write a note(if any)")

if st.button("Save Expense"):
    if product and price > 0:
        add_expense(date, product, price, note)
        st.success(f"Successfully saved: {product} for ₹{price:.2f}")
        st.rerun()
    else:
        st.error("Please provide a Product name and price greater than 0.")

total_spent = get_total_expenses()
remaining_money = monthly_expense - total_spent

st.metric(label="Remaining Budget", value=f"{remaining_money:.2f}")

st.divider()

if st.checkbox("Show Saved Expenses"):
    conn = sql.connect("expenses.db")
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    st.dataframe(df)

if st.button("Clear Saved Expenses"):
    conn = sql.connect("expenses.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS expenses")
    c.execute("DROP TABLE IF EXISTS settings")
    conn.commit()
    conn.close()

    init_db()

    st.warning("All saved data has been cleared.")
    st.rerun()