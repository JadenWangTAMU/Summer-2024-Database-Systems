# Summer-2024-Database-Systems


To create the tables specified in the model (run this in terminal):
`$ python3
$ from app import app, db
  with app.app_context():
    db.create_all()`

Then, to run the SQL script:
1. Change your directory to where the script is located
2. Run this command in your terminal
   `psql -d artfolio_db -U postgres -f 10_paintings.sql`
3. You will be prompted to input your password for this user and database.
