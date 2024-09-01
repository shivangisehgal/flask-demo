from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app5 = Flask(__name__)
app5.secret_key = "secret"
app5.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app5.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app5)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

# Initialize database
with app5.app_context():
    db.create_all()  # This will create the table if it doesn't exist

@app5.route("/")
def home():
    return "go to login bro"

@app5.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["user"] = request.form["nm"]
        user = session["user"]  # Fix: get the user from the session

        found_user = users.query.filter_by(name=user).first()

        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")  # empty email
            db.session.add(usr)
            db.session.commit()

        return redirect(url_for("user"))

    else:
        if "user" in session:
            myusername = session["user"]
            return redirect(url_for("user"))
        else:
            return render_template("form4.html")

@app5.route("/userPage", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        myusername = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email

            found_user = users.query.filter_by(name=myusername).first()
            if found_user:
                found_user.email = email
                db.session.commit()

            flash("Email was saved!")

        else:
            if "email" in session:
                email = session["email"]

        return render_template("form5.html", email=email, nm=myusername)
    else:
        flash("you are not logged in!")
        return redirect(url_for("login"))

@app5.route("/viewDB")
def view():
    return render_template("viewdb5.html", values=users.query.all())

@app5.route("/logout")
def logout():
    session.pop("user", None)  # if user exists, else default is none 
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app5.run(debug=True, port=4085)

#########################

# blueprints
# in auth.py
# auth = Blueprint('auth', __name__)


# in app.py
# app.register_blueprint(auth, url_prefix='/auth')