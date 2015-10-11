import psycopg2
import os
import simplejson as json

# Dummy for local deployment
# Remove when deploying to Heroku

TRANSACTION_TABLE="Transaction"
dbname=os.environ['DBNAME']
dbuser=os.environ['DBUSER']
dbpass=os.environ['DBPASS']
dbhost=os.environ['DBHOST']

conn = psycopg2.connect("dbname='"+dbname+"' user='"+dbuser+"' host='"+dbhost+"' password='"+dbpass+"'")
cur=conn.cursor()  


def get_total_amount(userName):
    cur.execute("SELECT Account.amount_held FROM Account WHERE Account.username='"+userName+"';")
    
    for row in cur.fetchall():
        return row[0];

def get_transactions_for_id(userName):
    
    cur.execute("SELECT * FROM Transaction WHERE Transaction.fromUser='"+userName+"' OR Transaction.toUser='"+userName+"';")
    
    #transactionId, fromUser, toUser, amount, transDate
    data = {}
    lst=[]
    
    for row in cur.fetchall():
        data['transactionId'] = row[0]
        data['fromUser'] = row[1]
        data['toUser'] = row[2]
        data['amount'] = row[3]
        data['transDate'] = row[4]
        lst.append(data)

    return json.dumps(lst)

def main():
    print(get_transactions_for_id("divyesh"))
    print(get_total_amount("divyesh"))

if __name__ == "__main__":
    main()
