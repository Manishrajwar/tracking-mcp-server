from email import mime
from fastmcp import FastMCP
import os
import sqlite3
import logging

logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), "expense_tracker.log"),
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

mcp = FastMCP("expenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)

init_db()

@mcp.tool
def add_expense(amount :float, category : str, subcategory : str, date : str, description : str):
    """add a new expense"""
    logging.info(f"Adding expense: amount={amount}, category={category}, subcategory={subcategory}, date={date}, description={description}")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO expenses (amount, category, subcategory, date, description)
            VALUES (?, ?, ?, ?, ?)
        """, (amount, category, subcategory, date, description))

    return f"Expense added: {amount} on {date}"

@mcp.tool
def get_expenses(category:str | None = None, subcategory:str | None = None, date:str | None = None):
    """Get expenses from the database"""
    logging.info(f"Getting expenses: category={category}, subcategory={subcategory}, date={date}")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM expenses WHERE 1=1"
        params = []

        if category:
            query += " AND category = ?"
            params.append(category)
        
        if subcategory:
            query += " AND subcategory = ?"
            params.append(subcategory)

        if date:
            query += " AND date = ?"
            params.append(date)

        query += " ORDER BY date DESC"

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        if not rows:
            return "No expenses found."

        # Format the output
        result = "Expenses:\n"
        for row in rows:
            # Assuming columns are: id, amount, category, subcategory, date, description
            result += f"- {row[4]} | {row[1]:.2f} | {row[2]} > {row[3]} | {row[5]}\n"
        
        return result

@mcp.tool
def delete_expenses(id:int | None = None , date:str | None = None , category :str| None = None):
    """delete expense from the database"""
    logging.info(f"Deleting expense: id={id}, date={date}, category={category}")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = "DELETE FROM expenses WHERE 1=1"
        params = []

        if id:
            query += " AND id = ?"
            params.append(id)
        
        if date:
            query += " AND date = ?"
            params.append(date)

        if category:
            query += " AND category = ?"
            params.append(category)

        cursor.execute(query, tuple(params))
        conn.commit()

        return f"Expense deleted: {id}"
    
@mcp.tool
def update_expense(id:int, amount:float|None=None , category: str|None=None, subcategory: str|None=None, date: str|None=None, description: str|None=None):
    """update expense in the database"""
    logging.info(f"Updating expense: id={id}, amount={amount}, category={category}, subcategory={subcategory}, date={date}, description={description}")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = "UPDATE expenses SET 1=1"
        params = []

        if amount:
            query += " AND amount = ?"
            params.append(amount)
        
        if category:
            query += " AND category = ?"
            params.append(category)

        if subcategory:
            query += " AND subcategory = ?"
            params.append(subcategory)

        if date:
            query += " AND date = ?"
            params.append(date)

        if description:
            query += " AND description = ?"
            params.append(description)

        query += " WHERE id = ?"
        params.append(id)

        cursor.execute(query, tuple(params))
        conn.commit()

        return f"Expense updated: {id}"

@mcp.resource("expense://categories" , mime_type="application/json")
def get_categories():
    logging.debug("Fetching categories resource")
    categories_path = os.path.join(os.path.dirname(__file__), "categories.json")
    with open(categories_path, "r" , encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    # mcp.run()
    mcp.run(transport="http", port=9000 , host="0.0.0.0")