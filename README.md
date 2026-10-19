# Expense Tracker

A simple personal expense tracking application built with Python and Streamlit. It lets you record daily spending, save the entries in SQLite, and review previously saved expenses in a table.

## Features

- Add expense date, product name, price, and notes
- Save expenses to a local SQLite database
- View saved transactions in a table
- Clear all saved records from the database
- Simple and lightweight interface for personal budgeting

## Tech Stack

- Python
- Streamlit
- SQLite
- Pandas
- Plotly

## Project Structure

```text
Expense-Tracker/
├── main.py
├── expenses.db
├── README.md
└── ...
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/HetLakhani111/Expense-Tracker.git
cd Expense-Tracker
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install streamlit pandas plotly
```

## Run the App

From the project folder, start the Streamlit app:

```bash
streamlit run main.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## How It Works

- The app creates an `expenses.db` SQLite database automatically when started.
- Each expense entry includes:
  - date
  - product name
  - price
  - note
- You can toggle the saved expenses table from the app interface.
- Use the clear button to reset all saved data.

## Features to be Added

Planned enhancements for this project include:

- monthly expense summaries
- category-based tracking
- charts and analytics dashboard
- CSV export and import
- budget alerts and spending limits
- search and filter by date or product

## Notes

This project is designed as a lightweight personal expense tracker and can be extended with:

- monthly summaries
- category-based filtering
- charts and analytics
- CSV export
- authentication for multi-user use

## License

This project is for personal use and learning purposes.
