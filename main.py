from flask import Flask, render_template, redirect, url_for, request, abort
from validation.login import validate

app = Flask(__name__)

LENDER = "lender"
CLIENT = "borrower"


@app.route("/")
def main():
    return redirect(url_for('login'))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/lender")
def lender():
    return render_template("lender.html")

@app.route("/client")
def client():
    return render_template("borrower.html")

@app.route("/auth", methods=["POST"])
def auth():
    username = request.form["username"]
    password = request.form["password"]
    print validate(username, password)

    if validate(username, password) == LENDER:
        return redirect(url_for('lender'))
    if validate(username, password) == CLIENT:
        return redirect(url_for('client'))
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
