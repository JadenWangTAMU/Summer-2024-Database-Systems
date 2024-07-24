from multiprocessing import synchronize
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy import exc
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:<password>@localhost/artfolio_db' #replace with your own password
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    title=db.Column(db.String(100))
    year_finished=db.Column(db.Integer)
    cost=db.Column(db.Float)
    description=db.Column(db.String(100))
    photo_link=db.Column(db.String(200))
    sellable=db.Column(db.Boolean)
    viewable=db.Column(db.Boolean)

class creator(db.Model):
    creator_id=db.Column(db.Integer, primary_key=True)
    creator_fname=db.Column(db.String(100))
    creator_lname=db.Column(db.String(100))
    birth_country=db.Column(db.String(100))
    birth_date=db.Column(db.String(100))
    death_date=db.Column(db.String(100))

class user(db.Model):
    user_id=db.Column(db.Integer, primary_key=True)
    user_fname=db.Column(db.String(100))
    user_lname=db.Column(db.String(100))
    email=db.Column(db.String(100))
    password=db.Column(db.String(100))
    role=db.Column(db.String(100))

class transaction(db.Model):
    transaction_id=db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    timestamp=db.Column(db.Datetime)

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug = True)

def get_art_pieces():
    query = select(art_piece)
    result = db.session.execute(query)

    art_piece_list = []
    for art_piece in result.scalars():
        art_piece_list.append((art_piece.cname, art_piece.addr, art_piece.phone))
    
    for art_piece in result.scalars():
        creator_id = art_piece.creator_id
        user_id = art_piece.user_id

        creator = get_creator_fromid(creator_id)
        user = get_user_fromid(user_id)

        art_piece_list.append((creator.fname, creator.lname, user.fname, user.lname, art_piece.title, art_piece.year_finished, art_piece.cost, art_piece.description, art_piece.photo_link, art_piece.sellable, art_piece.viewable))

    return art_piece_list

def get_creators():
    query = select(creator)
    result = db.session.execute(query)

    creator_list = []
    for creator in result.scalars():
        creator_list.append((creator.creator_fname, creator.creator_lname, creator.birth_country, creator.birth_date, creator.death_date))
    return creator_list

def get_users():
    query = select(user)
    result = db.session.execute(query)

    user_list = []
    for user in result.scalars():
        user_list.append((user.user_fname, user.user_lname, user.email, user.password, user.role))
    return user_list

def get_transactions():
    query = select(transaction)
    result = db.session.execute(query)

    transaction_list = []
    for transaction in result.scalars():
        buyer_id = transaction.buyer_id
        seller_id = transaction.seller_id

        buyer = get_user_fromid(buyer_id)
        seller = get_user_fromid(seller_id)

        transaction_list.append((buyer.fname, buyer.lname, seller.fname, seller.lname, transaction.timestamp))

    return transaction_list

def get_creator_fromid(creator_id):
    query = select(creator).where(creator.creator_id==creator_id)
    result = db.session.execute(query)
    creator = result.scalar()
    if creator is None:
        raise('Creator not found')
    return creator

def get_user_fromid(user_id):
    query = select(user).where(user.user_id==user_id)
    result = db.session.execute(query)
    user = result.scalar()
    if user is None:
        raise('User not found')
    return user
