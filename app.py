from multiprocessing import synchronize
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy import exc
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Burri123456@localhost:5432/artfolio_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)
app.app_context().push()

class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True)
    user_fname = db.Column(db.String(100))
    user_lname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    role = db.Column(db.String(100))

class Creator(db.Model):
    __tablename__ = 'Creator'
    creator_id = db.Column(db.Integer, primary_key=True)
    creator_fname = db.Column(db.String(100))
    creator_lname = db.Column(db.String(100))
    birth_country = db.Column(db.String(100))
    birth_date = db.Column(db.String(100))
    death_date = db.Column(db.String(100))

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    timestamp = db.Column(db.DateTime)

class Art_Piece(db.Model):
    piece_id=db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('Creator.creator_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    title=db.Column(db.String(100))
    year_finished=db.Column(db.Integer)
    cost=db.Column(db.Float)
    description=db.Column(db.String(100))
    photo_link=db.Column(db.String(200))
    sellable=db.Column(db.Boolean)
    viewable=db.Column(db.Boolean)

@app.route("/")
def home():
    return render_template("home.html")

db.create_all()

if __name__ == '__main__':
    app.run()