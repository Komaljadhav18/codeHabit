from flask import Flask, request, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# ---------- Paths ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # BackEnd folder
ROOT_DIR = os.path.dirname(BASE_DIR)                   # codeHabit folder
DB_PATH = os.path.join(BASE_DIR, "users.db")          # DB in BackEnd

# ---------- DATABASE ----------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    return conn

# ---------- SERVE INDEX.HTML ----------
@app.route("/")
def home():
    # serve index.html from ROOT_DIR
    return send_from_directory(ROOT_DIR, 'index.html')

# ---------- SERVE CSS & JS ----------
@app.route('/styling/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(ROOT_DIR, 'styling'), filename)

@app.route('/JS/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(ROOT_DIR, 'JS'), filename)

# ---------- SIGNUP ----------
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    if cur.fetchone():
        conn.close()
        return "Username already exists"

    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return "Signup successful"

# ---------- LOGIN ----------
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    conn.close()
    if user:
        return "Login successful"
    else:
        return "Invalid username or password"

# ---------- RUN ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



