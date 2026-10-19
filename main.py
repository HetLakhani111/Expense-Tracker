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

init_db()

st.title("Expense Tracker")

date = st.date_input(label="Date", value="today")
product = st.text_input(label="Product Name", placeholder="Enter Product Name")
price = st.number_input(label="Price", placeholder="Enter price of the product")
note = st.text_input(label="Note", placeholder="Write a note(if any)")

if st.button("Save Expense"):
    if product and price > 0:
        add_expense(date, product, price, note)
        st.success(f"Successfully saved: {product} for ₹{price:.2f}")
    else:
        st.error("Please provide a Product name and price greater than 0.")

if st.checkbox("Show Saved Expenses"):
    conn = sql.connect("expenses.db")
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    st.dataframe(df)

if st.button("Clear Saved Expenses"):
    conn = sql.connect("expenses.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS expenses")
    conn.commit()
    conn.close()

    init_db()

    st.warning("All saved data has been cleared.")
    st.rerun()