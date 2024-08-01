# Summer-2024-Database-Systems

## Requirements
- Python 3.8 or higher
- Flask
- SQLAlchemy
- Flask-SQLAlchemy
- psycopg2-binary
- PostgresSQL 16 or higher

## External Deps
- Tembo (used to host a Postgres database in the cloud) (https://tembo.io/)
- Github (used to host the code) (https://www.github.com/)

## Installation
Download the application code from Github
`git clone https://github.com/JadenWangTAMU/Summer-2024-Database-Systems.git`





To create the tables specified in the model (run this in terminal):
```
$ python3
$ from app import app, db
  with app.app_context():
    db.create_all()
```

Then, to run the SQL script:
1. Change your directory to where the script is located
2. Run this command in your terminal
   `$ psql -d artfolio_db -U postgres -f 10_paintings.sql`
3. You will be prompted to input your password for this user and database.


# changes made since last time
- I messed up the photo links for each painting. Updated them so that they actually show up when viewing the paintings.
- The character limit on these photo links was too small, so I increased it to 1000 characters.
- Other than that, everything should work...

# changes part 2 
- found a way to have a PostgresSQL server in the cloud
- now everyone should be able to connect to the same database 