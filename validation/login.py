import psycopg2
import os

# Dummy for local deployment
# Remove when deploying to Heroku
# os.environ['DBNAME'] = "fintech"
# os.environ['DBUSER'] = ""
# os.environ['DBPASS'] = ""
# os.environ['DBHOST'] = "localhost"
# ##################################

LOGIN_TABLE="LoginInfo"
dbname=os.environ['DBNAME']
dbuser=os.environ['DBUSER']
dbpass=os.environ['DBPASS']
dbhost=os.environ['DBHOST']

conn = psycopg2.connect("dbname='"+dbname+"' user='"+dbuser+"' host='"+dbhost+"' password='"+dbpass+"'")
cur=conn.cursor()

# Displays the table specified by tablename argument
def display_table(tablename):
    cur.execute("SELECT * FROM "+tablename)
    for row in cur.fetchall():
        print row[0]+" "+row[1]+" "+row[2]+" "+row[3]

# Inserts the username, password and the role in the LoginInfo table. Returns True if insertion was successful, Else False
def insert_login_info(username, name, password, role):
    try:
        cur.execute("INSERT INTO "+LOGIN_TABLE+" VALUES('"+username+"','"+name+"','"+password+"','"+role+"');");
    except:
        return False
    return True

# Validates whether the username-password-role combination is present in database and correct
def validate(username, password):
    cur.execute("SELECT * FROM "+LOGIN_TABLE)
    for row in cur.fetchall():
        if row[0]==username and row[2]==password:
            return row[3]
    return False
