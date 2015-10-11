import psycopg2
import os,traceback,sys
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

def print_transactions():
    cur.execute("SELECT * FROM Transaction")
    for row in cur.fetchall():
        print(row[0]+" "+row[1]+" "+row[2]+" "+str(row[3])+" "+row[4]+" "+row[5])

def insert_transaction(transactionId, fromUser, toUser, amount, transDate, description):
    try:
        cur.execute("INSERT INTO Transaction (transactionid, fromuser, touser, amount, transdate, status) VALUES ('"+transactionId+"','"+fromUser+"','"+toUser+"',"+str(amount)+",'"+transDate+"','"+description+"');")
        print "Inside Insert";
        conn.commit();
    except :
        print "Insertion Error"
        traceback.print_exc(file=sys.stdout)

def get_total_amount(userName):
    cur.execute("SELECT * FROM Account WHERE Account.username='"+userName+"';")
    
    for row in cur.fetchall():
        return row;

def get_user_info(userName):
    cur.execute("SELECT * FROM loginInfo WHERE loginInfo.username='"+userName+"';")
    for row in cur.fetchall():
        return row;

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
    insert_transaction("t008", "username1","receiver1","5694","06/04/2012","Success")
    print_transactions()
    conn.commit()

if __name__ == "__main__":
    main()
