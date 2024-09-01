
from flask import Flask, redirect, url_for

app2 = Flask(__name__)

@app2.route("/")
def home():
    return "Hello! this is the main page <h1>HELLO<h1>"

@app2.route("/<name>")
def user(name):
    return f"Hello {name}!"

@app2.route("/admin")
def admin():
    return redirect(url_for("user", name="Admin!")) #redirect takes in the function name

if __name__ == "__main__":
    app2.run()