from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

bcrypt = Bcrypt(app)

# ---------------- DATABASE INIT ----------------
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            conn = sqlite3.connect("users.db")
            c = conn.cursor()

            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, hashed_password))

            conn.commit()
            conn.close()

            return redirect("/login")

        except sqlite3.IntegrityError:
            return "Username already exists ❌"

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = c.fetchone()

        conn.close()

        if user and bcrypt.check_password_hash(user[0], password):
            session["user"] = username   # store user session
            return redirect("/dashboard")
        else:
            return "Invalid credentials ❌"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"])
    return redirect("/login")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)