from flask import Flask, render_template, redirect, url_for, request, abort

app = Flask(__name__)

LENDER = "lenders"
CLIENT = "borrowers"


def validate(username, password):
    print username, password
    return CLIENT

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

    if validate(username, password) == LENDER:
        return redirect(url_for('lender'))
    if validate(username, password) == CLIENT:
        return render_template("borrower.html")
    return redirect(url_for('client'))


if __name__ == "__main__":
    app.run(debug=True)
