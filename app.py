from multiprocessing import synchronize
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy import exc
from datetime import datetime
import psycopg2


#not sure if this actually initalizes the database
def init_db():
    with app.app_context():
        db.create_all()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:M1Pb6czhH8zRSfvB@stably-heuristic-elk.data-1.use1.tembo.io:5432/postgres'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

#psql 'postgresql://postgres:M1Pb6czhH8zRSfvB@stably-heuristic-elk.data-1.use1.tembo.io:5432/postgres'

# old connection string: 'postgresql://postgres:password!@localhost:5432/artfolio_db'

db = SQLAlchemy(app)

class art_piece(db.Model):
    piece_id=db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.creator_id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), default = 1)
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
    birth_date=db.Column(db.Date)
    death_date=db.Column(db.Date)

class user(db.Model):
    user_id=db.Column(db.Integer, primary_key=True)
    user_fname=db.Column(db.String(100))
    user_lname=db.Column(db.String(100))
    email=db.Column(db.String(100), unique=True)
    password=db.Column(db.String(100))
    role=db.Column(db.String(1))

class transaction(db.Model):
    transaction_id=db.Column(db.Integer, primary_key=True)
    piece_id = db.Column(db.Integer, db.ForeignKey('art_piece.piece_id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    timestamp=db.Column(db.DateTime, default=datetime.utcnow)

init_db()

@app.route("/")
def index():
    return render_template("index.html")

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


#this is the main function that runs the app
if __name__ == '__main__':
    app.run(debug = True)