from flask import Flask, render_template, redirect, url_for, request, abort
# from validation.login import validate
from sns.send import addtotable, sendtotable

#import transaction
import os

app = Flask(__name__)

LENDER = "lender"
CLIENT = "borrower"

borrowers = {
    "+5211553788466" : "798c038792891ae421d8987f8c3d3d354566785648655dd09599237c0eafa7e7",
    "+5217222842257" : "91b56d30714be8be162da744c2503f7aad199d3d937db31fa6d0e0de0a9a2c71"
};

dbname=os.environ['DBNAME']
dbuser=os.environ['DBUSER']
dbpass=os.environ['DBPASS']
dbhost=os.environ['DBHOST']

conn = psycopg2.connect("dbname='"+dbname+"' user='"+dbuser+"' host='"+dbhost+"' password='"+dbpass+"'")
cur=conn.cursor()

def insert_transaction(transactionId, fromUser, toUser, amount, transDate, description):
    try:
        cur.execute("INSERT INTO Transaction (transactionid, fromuser, touser, amount, transdate, status) VALUES ('"+transactionId+"','"+fromUser+"','"+toUser+"',"+str(amount)+",'"+transDate+"','"+description+"');")
    except:
        print "Insertion Error"

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
    requesterId=transactions['requesterId']

    for transaction in sendentries:
        tid=transaction['id']
        accountId = transaction['accountId'];
        amount=transaction['amount']
        tdate=transaction['transactionDate']
        desc=transaction['description']
        
        insert_transaction(tid,accountId,requesterId,amount,tdate,desc)

        if(borrowers.get(accountId) != None):
            addtotable(borrowers.get(accountId))
            newEntry = {};
            newEntry['token'] = borrowers.get(accountId);
            newEntry['message'] = "Hi! You have received amount of " + str(transaction['amount']) + " from  Modern Money. Wish you good luck from Modern."
            print(newEntry);
            sendtotable(newEntry);
        
       
    return "done send!"


@app.route('/client/saveTransactions', methods=['POST'])
def saveTransactionsForClient():
   # print(request.get_json(force=True));
    transactions = request.get_json(force=True)
    sendentries = transactions['requests'];

    for transaction in sendentries:
        accountId = transaction['accountId'];
        if(borrowers.get(accountId) != None):
            addtotable(borrowers.get(accountId))
            newEntry = {};
            newEntry['token'] = borrowers.get(accountId);
            newEntry['message'] = "Hi! You have received amount of " + str(transaction['amount']) + " from  Modern Money. Wish you good luck from Modern."
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
def client1():
    return render_template("borrower.html")

@app.route("/client/2")
def client2():
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
    app.run(debug=True, port=port,host="0.0.0.0")
