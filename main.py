from flask import Flask, render_template, redirect, url_for, request, abort
# from validation.login import validate
from sns.send import addtotable, sendtotable
import os

app = Flask(__name__)

LENDER = "lender"
CLIENT = "borrower"

#tokenSpecific = "798c038792891ae421d8987f8c3d3d354566785648655dd09599237c0eafa7e7"
tokenSpecificGiri = "91b56d30714be8be162da744c2503f7aad199d3d937db31fa6d0e0de0a9a2c71";

@app.route("/")
def main():
    return redirect(url_for('lender'))

@app.route('/send', methods=['GET', 'POST'])
def sendstuffs():
    sendentries = request.get_json(force=True)
    for token in sendentries:
        addtotable(token["token"])
        sendtotable(token)
    return "done send!"

@app.route('/saveTransactions', methods=['GET', 'POST'])
def saveTransactions():
   # print(request.get_json(force=True));
    transactions = request.get_json(force=True)
    sendentries = transactions['requests'];

    for transaction in sendentries:
        addtotable(tokenSpecificGiri)
        newEntry = {};
        newEntry['token'] = tokenSpecificGiri;
        newEntry['message'] = "Hi! You have received amount of " + str(transaction['amount']) + " from Modern Money. Wish you good luck from Modern."
        print(newEntry);
        sendtotable(newEntry);
    return "done send!"


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/lender")
def lender():
    return render_template("lender.html")

@app.route("/client/1")
def client():
    return render_template("borrower.html")

@app.route("/client/2")
def client():
    return render_template("borrower1.html")

@app.route("/auth", methods=["POST"])
def auth():
    username = request.form["username"]
    password = request.form["password"]

    if validate(username, password) == LENDER:
        return redirect(url_for('lender'))
    if validate(username, password) == CLIENT:
        return redirect(url_for('client'))
    return redirect(url_for('login'))


port = int(os.environ.get('PORT', 5000))
if __name__ == "__main__":
    app.run(debug=True, port=port)
