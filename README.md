# Expense Tracker

A simple personal expense tracking application built with Python and Streamlit. It lets you record daily spending, save the entries in SQLite, and review previously saved expenses in a table.

## Features

- Add expense date, product name, price, and notes
- Save expenses to a local SQLite database
- View saved transactions in a table
- Set and save a monthly budget
- See remaining budget based on the total of saved expenses
- Clear all saved expenses and the saved budget
- Simple, lightweight interface for personal budgeting

## Tech Stack

- Python
- Streamlit
- SQLite
- Pandas

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
- Expense records and the monthly budget are stored in this database.
- Each expense entry includes:
  - date
  - product name
  - price
  - note
- Set the monthly budget in the app; it is saved and loaded the next time you run the app.
- The remaining budget is calculated as the monthly budget minus the sum of all saved expenses.
- You can toggle the saved expenses table from the app interface.
- Use **Clear Saved Expenses** to delete all expense records and reset the saved budget.

## Features to be Added

Planned enhancements for this project include:

- monthly expense summaries
- category-based tracking
- charts and analytics dashboard
- CSV export and import
- search and filter by date or product
- budget alerts and spending limits

## Notes

This project is designed as a lightweight personal expense tracker and can be extended with:

- monthly summaries
- category-based filtering
- charts and analytics
- CSV export
- authentication for multi-user use

## License

This project is for personal use and learning purposes.
