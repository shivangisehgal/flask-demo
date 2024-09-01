from flask import Flask, redirect, url_for, render_template

app3 = Flask(__name__)

@app3.route("/")
def home():
    return "Go to any user path"
@app3.route("/<name>")
def user(name):
    return render_template("codefor3.html", content=["tim", "joe", "bill"])

if __name__ == "__main__":
    app3.run(debug=True, port=4080)