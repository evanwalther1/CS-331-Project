import os
import secrets
import sqlite3
from pathlib import Path

from flask import Flask, flash, redirect, render_template_string, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

DATABASE = Path(__file__).with_name("users.db")

PAGE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Password authentication demo</title>
  </head>
  <body>
    <h1>Password authentication demo</h1>
    {% for message in get_flashed_messages() %}
      <p>{{ message }}</p>
    {% endfor %}

    {% if username %}
      <p>You are signed in as <strong>{{ username }}</strong>.</p>
      <form method="post" action="{{ url_for('logout') }}">
        <button type="submit">Log out</button>
      </form>
    {% else %}
      <h2>Create account</h2>
      <form method="post" action="{{ url_for('register') }}">
        <label>Username <input name="username" required maxlength="50" autocomplete="username"></label>
        <label>Password <input type="password" name="password" required minlength="8" autocomplete="new-password"></label>
        <button type="submit">Register</button>
      </form>

      <h2>Sign in</h2>
      <form method="post" action="{{ url_for('login') }}">
        <label>Username <input name="username" required autocomplete="username"></label>
        <label>Password <input type="password" name="password" required autocomplete="current-password"></label>
        <button type="submit">Log in</button>
      </form>
    {% endif %}
  </body>
</html>
"""


def connect_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with connect_db() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
            """
        )


@app.get("/")
def home():
    return render_template_string(PAGE, username=session.get("username"))


@app.post("/register")
def register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or len(username) > 50 or len(password) < 8:
        flash("Enter a username (up to 50 characters) and a password of at least 8 characters.")
        return redirect(url_for("home"))

    try:
        with connect_db() as connection:
            connection.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
    except sqlite3.IntegrityError:
        flash("That username is already registered.")
        return redirect(url_for("home"))

    flash("Account created. You can now sign in.")
    return redirect(url_for("home"))


@app.post("/login")
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    with connect_db() as connection:
        user = connection.execute(
            "SELECT username, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if user is None or not check_password_hash(user["password_hash"], password):
        flash("Invalid username or password.")
        return redirect(url_for("home"))

    session.clear()
    session["username"] = user["username"]
    return redirect(url_for("home"))


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
