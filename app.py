from multiprocessing import synchronize
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy import exc
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:p@ssword!@localhost/artfolio' #replace with your own password
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)
app.app_context().push()

@app.route("/")
def hello():
    return "Hello, World!"


class art_piece(db.Model):
    piece_id=db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.creator_id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    title=db.Column(db.String(100))
    year_finished=db.Column(db.Integer)
    cost=db.Column(db.Float)
    description=db.Column(db.String(200))
    photo_link=db.Column(db.String(200))
    sellable=db.Column(db.Boolean)
    viewable=db.Column(db.Boolean)

class creator(db.Model):
    creator_id=db.Column(db.Integer, primary_key=True)
    creator_fname=db.Column(db.String(100))
    creator_lname=db.Column(db.String(100))
    birth_country=db.Column(db.String(100))
    birth_date=db.Column(db.Date)
    death_date=db.Column(db.Date)

class user(db.Model):
    user_id=db.Column(db.Integer, primary_key=True)
    user_fname=db.Column(db.String(100))
    user_lname=db.Column(db.String(100))
    email=db.Column(db.String(100))
    password=db.Column(db.String(100))
    role=db.Column(db.String(100))

class transaction(db.Model):
    transaction_id=db.Column(db.Integer, primary_key=True)
    piece_id = db.Column(db.Integer, db.ForeignKey('art_piece.piece_id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    timestamp=db.Column(db.DateTime)

if __name__ == '__main__':
    app.run()