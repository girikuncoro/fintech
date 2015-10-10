Financial Tech Hackathon at Cornell Tech on 9-11 October 2015, New York.

## Setup
This project is currently configured for OSx/Unix.

## Requirements
- Python 2.7x
- MySQL

## Configuration
- Put all dependencies under `requirements.txt`
- Perform installation dependencies `pip install -r requirements.txt`
- Install MySQL Server and Client by sudo apt-get install mysql-client-5.5 mysql-server-5.5 
- Install MySQL for python by sudo apt-get install python-mysqldb
- Open mysql by: mysql -u uname -p, type Password
- CREATE TABLE LoginInfo(username VARCHAR(45) PRIMARY KEY, password VARCHAR(45), role VARCHAR(20), CHECK(role='borrower' or role='lender')); 

## Run
- `python main.py`
- Open browser at `http://localhost:5000`

## Development Note
- Make new branch for every issue and merge to master
- validation Folder has login.py having display, validation and insertion functions.
