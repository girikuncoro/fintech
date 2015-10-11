from flask import Flask, render_template, redirect, url_for, request, abort
# from validation.login import validate
from sns.send import addtotable, sendtotable
import os,sys
sys.path.insert(0, './transaction')
from transaction import insert_transaction
from transaction import get_total_amount
from transaction import get_user_info
from transaction import get_transactions_for_id

import os,simplejson

#import transaction
import os

app = Flask(__name__)

LENDER = "lender"
CLIENT = "borrower"

borrowers = {
    "+5211553788466" : "712c7093bc2b7832278f09d10f8056bf5b32791f24430360a6e545ce7a5a4e86",
    "+5217222842257" : "a018ab635790a929d89295d9c5bcf7de51bccace7d822defef79321597d3d64a"
};

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
        print "Inside transaction";
        insert_transaction(tid,requesterId,accountId,amount,tdate,desc)

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

@app.route("/client1")
def client1():
    return render_template("borrower.html")

@app.route("/client2")
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


@app.route('/userInfo',methods=["POST"])
def getUserInfo() :
    userId = request.get_json(force=True);
    result = get_total_amount(userId['userId']);
    userInfo = get_user_info(userId['userId']);
    userInformation = {};
    userInformation['accountId'] = userInfo[0];
    userInformation['balance'] = getRemainingBalance(result[1],userId['userId']);
    userInformation['currency'] = result[2];
    userInformation['name'] = userInfo[1];
    userInformation['role'] = userInfo[3]; 
    
    return simplejson.dumps(userInformation);

def getRemainingBalance(totalBalance,userId):
    data  = get_transactions_for_id(userId);
    for trans in data:
        print(trans['amount']);
        if(trans['toUser'] == userId):
            totalBalance+=trans['amount'];
        else:
            totalBalance-=trans['amount'];    
    return totalBalance;    
@app.route('/getTransactions/<userId>',methods=["GET"])
def getTransactions(userId):
   # userId = request.get_json(force=True);
    data= get_transactions_for_id(userId);
    return simplejson.dumps(data);

port = int(os.environ.get('PORT', 5000))
if __name__ == "__main__":
    app.run(debug=True, port=port,host="0.0.0.0")
