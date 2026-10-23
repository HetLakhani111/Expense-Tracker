import streamlit as st
import plotly.express as px
import pandas as pd
import sqlite3 as sql
from datetime import date, datetime

DB_NAME = "expenses.db"


def init_db():
    with sql.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                product TEXT,
                price REAL,
                note TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value REAL
            )
        """)


def get_monthly_budget():
    with sql.connect(DB_NAME) as conn:
        row = conn.execute(
            "SELECT value FROM settings WHERE key = 'monthly_budget'"
        ).fetchone()
    return row[0] if row else 0.0


def set_monthly_budget(amount):
    with sql.connect(DB_NAME) as conn:
        conn.execute("""
            INSERT INTO settings (key, value)
            VALUES ('monthly_budget', ?)
            ON CONFLICT(key)
            DO UPDATE SET value = excluded.value
        """, (amount,))


def add_expense(expense_date, product, price, note):
    with sql.connect(DB_NAME) as conn:
        conn.execute("""
            INSERT INTO expenses (date, product, price, note)
            VALUES (?, ?, ?, ?)
        """, (
            expense_date.strftime("%Y-%m-%d"),
            product,
            price,
            note
        ))


def get_monthly_expenses():
    current_month = date.today().strftime("%Y-%m")

    with sql.connect(DB_NAME) as conn:
        df = pd.read_sql_query("""
            SELECT *
            FROM expenses
            WHERE strftime('%Y-%m', date) = ?
            ORDER BY date DESC, id DESC
        """, conn, params=(current_month,))

    return df


# Initialize database
init_db()

# Page
st.title("Expense Tracker")

# Monthly budget
saved_budget = get_monthly_budget()

monthly_budget = st.number_input(
    "Monthly Budget (₹)",
    min_value=0.0,
    value=float(saved_budget),
    step=100.0
)

if monthly_budget != saved_budget:
    set_monthly_budget(monthly_budget)
    st.toast("Monthly budget updated!")

st.divider()

# Add expense
st.subheader("Add Expense")

expense_date = st.date_input("Date", value=date.today())
product = st.text_input(
    "Product Name",
    placeholder="Enter product name"
)
price = st.number_input(
    "Price (₹)",
    min_value=0.0,
    step=10.0,
    format="%.2f"
)
note = st.text_input("Note", placeholder="Optional note")

if st.button("Save Expense"):
    if product.strip() and price > 0:
        add_expense(expense_date, product.strip(), price, note)
        st.success(f"Saved {product}: ₹{price:.2f}")
        st.rerun()
    else:
        st.error("Enter a product name and a price greater than zero.")

st.divider()

# Current month's expenses
df = get_monthly_expenses()

total_spent = float(df["price"].sum()) if not df.empty else 0.0
remaining_budget = monthly_budget - total_spent

# Budget metrics
col1, col2 = st.columns(2)

col1.metric("Monthly Spending", f"₹{total_spent:,.2f}")
col2.metric("Remaining Budget", f"₹{remaining_budget:,.2f}")

# Budget pie chart
st.subheader("Monthly Budget Overview")

if monthly_budget > 0:
    spent_for_chart = min(total_spent, monthly_budget)
    remaining_for_chart = max(monthly_budget - total_spent, 0)

    chart_data = pd.DataFrame({
        "Category": ["Spent", "Remaining Budget"],
        "Amount": [spent_for_chart, remaining_for_chart]
    })

    # Hide zero-value slices
    chart_data = chart_data[chart_data["Amount"] > 0]

    fig = px.pie(
        chart_data,
        names="Category",
        values="Amount",
        title="Spent vs Remaining Budget",
        hole=0.4,
        color="Category",
        color_discrete_map={
            "Spent": "#FF6B6B",
            "Remaining Budget": "#2ECC71"
        }
    )

    fig.update_traces(
        textinfo="label+percent",
        hovertemplate=(
            "%{label}<br>"
            "Amount: ₹%{value:,.2f}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    if total_spent > monthly_budget:
        st.error(
            f"You exceeded your budget by "
            f"₹{total_spent - monthly_budget:,.2f}."
        )
else:
    st.info("Set a monthly budget greater than ₹0 to display the chart.")

st.divider()

# Saved expenses
if st.checkbox("Show Saved Expenses"):
    if df.empty:
        st.info("No expenses recorded for this month.")
    else:
        st.dataframe(df, use_container_width=True)

# Clear all data
if st.button("Clear All Saved Data", type="secondary"):
    with sql.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM expenses")
        conn.execute("DELETE FROM settings")

    st.success("All saved expenses and budget settings have been cleared.")
    st.rerun()
