from flask import Flask, render_template

app = Flask(__name__)


# Show login page
@app.route("/")
def home():
    return render_template("login.html")


# Show registration page
@app.route("/register")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)