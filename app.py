from multiprocessing import synchronize
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy import exc
from datetime import datetime
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:gekkouga658Postgres@localhost:5432/artfolio_db' #replace with your own file
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:gekkouga658Postgres@localhost/artfolio_db' #replace with your own file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)
app.app_context().push()

class art_piece(db.Model):
    piece_id=db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.creator_id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    title=db.Column(db.String(100))
    year_finished=db.Column(db.Integer)
    cost=db.Column(db.Float)
    description=db.Column(db.String(200))
    photo_link=db.Column(db.String(1000))
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
    role=db.Column(db.String(1))

class transaction(db.Model):
    transaction_id=db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    timestamp=db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug = True)

@app.route('/paintings', methods = ['GET'])
def paintings():
    #used for page stuff
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '', type=str)
    sort_by = request.args.get('sort_by', 'title', type=str)
    #can change this to whatever, decides how many paintings are shown per page
    per_page = 5

    # does the user want to search for a painting?
    if query:
        #filter based on what they searched for
        paintings_query = art_piece.query.filter(art_piece.title.ilike(f'%{query}%'))
    else:
        #else just get all the paintings
        paintings_query = art_piece.query
    
    #find out how the user wants to sort the paintings and sort accordingly
    if sort_by == 'title':
        paintings_query = paintings_query.order_by(art_piece.title)
    elif sort_by == 'year':
        paintings_query = paintings_query.order_by(art_piece.year_finished)
    
    #paginate the paintings (basically separates them into pages)
    paintings = paintings_query.paginate(page=page, per_page=per_page)
    #get all the creators so we can display the artist of each painting
    all_creators = creator.query.all()
    #render the paintings page with all the required info
    return render_template("paintings.html", paintings = paintings.items, creators = all_creators, pagination = paintings, query=query, sort_by = sort_by)

@app.route('/transactions', methods = ['GET'])
def transactions():
    #used for page stuff
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '', type=str)
    sort_by = request.args.get('sort_by', 'title', type=str)
    #can change this to whatever, decides how many transactions are shown per page
    per_page = 5
    
    # does the user want to search for a transaction?
    if query:
        #filter based on what they searched for
        art_piece=art_piece.query.filter(art_piece.piece_id.ilike(f'%{transaction.piece_id}%'))
        transactions_query = transaction.query.filter(art_piece.title.ilike(f'%{query}%'))
    else:
        #else just get all the transactions
        transactions_query = transaction.query

    #find out how the user wants to sort the transactions and sort accordingly
    if sort_by == 'buyer_fname':
        buyer=get_user_fromid(transaction.buyer_id)
        transactions_query = transactions_query.order_by(buyer.user_fname)
    elif sort_by == 'buyer_lname':
        buyer=get_user_fromid(transaction.buyer_id)
        transactions_query = transactions_query.order_by(buyer.user_lname)
    elif sort_by == 'seller_fname':
        seller=get_user_fromid(transaction.seller_id_id)
        transactions_query = transactions_query.order_by(seller.user_fname)
    elif sort_by == 'seller_lname':
        seller=get_user_fromid(transaction.seller_id_id)
        transactions_query = transactions_query.order_by(seller.user_lname)
    elif sort_by == 'timestamp':
        transactions_query = transactions_query.order_by(transaction.timestamp)
    elif sort_by == 'title':
        art_piece=art_piece.query.filter(art_piece.piece_id.ilike(f'%{transaction.piece_id}%'))
        transactions_query = transactions_query.order_by(art_piece.title.ilike(f'%{query}%'))
    
    #paginate the paintings (basically separates them into pages)
    transactions = transactions_query.paginate(page=page, per_page=per_page)
    #get all the creators so we can display the artist of each painting
    all_users = user.query.all()
    #render the paintings page with all the required info
    return render_template("transactions.html", transactions = transactions.items, users = all_users, pagination = transactions, query=query, sort_by = sort_by)

@app.route('/users', methods = ['GET'])
def users():
    #used for page stuff
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort_by', 'lname', type=str)
    #can change this to whatever, decides how many users are shown per page
    per_page = 5
    
    users_query = user.query
    #find out how the user wants to sort the users and sort accordingly
    if sort_by == 'lname':
        users_query = users_query.order_by(user.user_lname)
    elif sort_by == 'fname':
        users_query = users_query.order_by(user.user_fname)
    elif sort_by == 'email':
        users_query = users_query.order_by(user.email)
    elif sort_by == 'role':
        users_query = users_query.order_by(user.role)
    
    #paginate the users (basically separates them into pages)
    users = users_query.paginate(page=page, per_page=per_page)
    #get all the creators so we can display the artist of each user
    #render the users page with all the required info
    return render_template("users.html", users = users.items, pagination = users, sort_by = sort_by)

#not sure if this actually initalizes the database
def init_db():
    with app.app_context():
        db.create_all()
