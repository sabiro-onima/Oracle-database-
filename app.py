from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# --- SQLite подключение ---
def get_conn():
    return sqlite3.connect("local.db")

# --- Главная страница ---
@app.route("/")
def index():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT
        )
    """)
    conn.commit()

    search = request.args.get("search", "")
    if search:
        cursor.execute("SELECT * FROM test_table WHERE value LIKE ?", (f"%{search}%",))
    else:
        cursor.execute("SELECT * FROM test_table")

    rows = cursor.fetchall()

    conn.close()

    return render_template("index.html", rows=rows)

# --- Страница просмотра SQLite --- 
@app.route("/sqlite")
def sqlite_page():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT
        )
    """)
    conn.commit()

    search = request.args.get("search", "")
    if search:
        cursor.execute("SELECT * FROM test_table WHERE value LIKE ?", (f"%{search}%",))
    else:
        cursor.execute("SELECT * FROM test_table")

    rows = cursor.fetchall()

    conn.close()

    return render_template("sqlite.html", rows=rows, search=search)

# --- Страница добавления записи ---
@app.route("/add", methods=["POST"])
def add():
    value = request.form.get("value")

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test_table (value) VALUES (?)", (value,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Oracle Cloud route removed — приложение работает только с локальной SQLite

if __name__ == "__main__":
    app.run(debug=True)
