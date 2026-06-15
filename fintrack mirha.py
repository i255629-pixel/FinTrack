import sqlite3
import matplotlib.pyplot as plt

DB = "finance.db"

def setup():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        type TEXT,
        category TEXT,
        amount REAL
    )
    """)

    conn.commit()
    conn.close()


def signup():
    username = input("Username: ")
    password = input("Password: ")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username, password)
        )

        conn.commit()
        print("Account created.")

    except:
        print("Username already exists.")

    conn.close()


def login():

    username = input("Username: ")
    password = input("Password: ")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cur.fetchone()

    conn.close()

    if user:
        dashboard(username)
    else:
        print("Invalid login")


def add_income(username):

    category = input("Income category: ")
    amount = float(input("Amount: "))

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO transactions(username,type,category,amount) VALUES(?,?,?,?)",
        (username, "Income", category, amount)
    )

    conn.commit()
    conn.close()

    print("Income added.")


def add_expense(username):

    category = input("Expense category: ")
    amount = float(input("Amount: "))

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO transactions(username,type,category,amount) VALUES(?,?,?,?)",
        (username, "Expense", category, amount)
    )

    conn.commit()
    conn.close()

    print("Expense added.")


def view_balance(username):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "SELECT SUM(amount) FROM transactions WHERE username=? AND type='Income'",
        (username,)
    )

    income = cur.fetchone()[0] or 0

    cur.execute(
        "SELECT SUM(amount) FROM transactions WHERE username=? AND type='Expense'",
        (username,)
    )

    expense = cur.fetchone()[0] or 0

    balance = income - expense

    print("\n----- SUMMARY -----")
    print("Income :", income)
    print("Expense:", expense)
    print("Balance:", balance)

    conn.close()


def expense_chart(username):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE username=? AND type='Expense'
        GROUP BY category
    """, (username,))

    data = cur.fetchall()

    conn.close()

    if not data:
        print("No expense data.")
        return

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Expense Breakdown")
    plt.show()


def dashboard(username):

    while True:

        print("\n===== FINTRACK DASHBOARD =====")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance")
        print("4. Expense Chart")
        print("5. Logout")

        choice = input("Choice: ")

        if choice == "1":
            add_income(username)

        elif choice == "2":
            add_expense(username)

        elif choice == "3":
            view_balance(username)

        elif choice == "4":
            expense_chart(username)

        elif choice == "5":
            break


def main():

    setup()

    while True:

        print("\n===== FINTRACK PRO =====")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")

        choice = input("Choice: ")

        if choice == "1":
            signup()

        elif choice == "2":
            login()

        elif choice == "3":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()