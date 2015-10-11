from flask import Flask, render_template, redirect, url_for, request, abort
from validation.login import validate
import os

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
    return render_template("index.html")

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


port = int(os.environ.get('PORT', 5000))
if __name__ == "__main__":
    app.run(debug=True, port=port, host="0.0.0.0")
