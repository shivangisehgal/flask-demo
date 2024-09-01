from flask import Flask, redirect, url_for, render_template, request, session

app4 = Flask(__name__)
app4.secret_key = "secret"

@app4.route("/")
def home():
    return "go to login bro"

@app4.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["user"] = request.form["nm"]
        return redirect(url_for("user"))
    else:
        if "user" in session:
            myusername = session["user"]
            return redirect(url_for("user"))
        return render_template("form4.html")

@app4.route("/userPage")
def user():
    if "user" in session:
        myusername = session["user"]
        return f"<h2> {myusername} </h2>"
    else:
        return redirect(url_for("login"))

@app4.route("/logout")
def logout():
    session.pop("user", None) #if user exists, else default is none 
    return redirect(url_for("login"))

if __name__ == "__main__":
    app4.run(debug=True, port=4088)

