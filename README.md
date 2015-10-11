## Project
Financial Tech Hackathon at Cornell Tech on 9-11 October 2015, New York. Heroku app url: http://stormy-dawn-1526.herokuapp.com

## Setup
This project is currently configured for OSx/Unix.

## Requirements
- Python 2.7
- Postgres 9.4.4

## Configuration
- Put all dependencies under `requirements.txt`
- Perform installation dependencies `pip install -r requirements.txt`
- Table for `postgres`:
```
CREATE TABLE LoginInfo(username VARCHAR(45) PRIMARY KEY, name VARCHAR(45), password VARCHAR(45), role VARCHAR(20), CHECK(role='borrower' or role='lender')); 
```

## Run
- `python main.py`
- Open browser at `http://localhost:5000`

## Development Note
- Make new branch for every issue and merge to master
- Validation Folder has login.py having display, validation and insertion functions
- Deploy heroku using `0.0.0.0` port, 1 dyno, and define `web: python main.py ${PORT}` in `Procfile`
