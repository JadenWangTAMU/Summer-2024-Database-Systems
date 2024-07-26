from multiprocessing import synchronize
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, inspect, text
from sqlalchemy import exc
from datetime import datetime
import psycopg2
import os


#checks if tables in the database are different from the ones in the models
def check_db():
    insepector = inspect(db.engine)
    existing_tables = insepector.get_table_names()
    model_tables = db.Model.metadata.tables.keys()
    if set(existing_tables) != set(model_tables):
        return True
    
    for table_name in model_tables:
        existing_columns = insepector.get_columns(table_name)
        model_columns = db.Model.metadata.tables[table_name].columns

        if len(existing_columns) != len(model_columns):
            return True
        
        for column in existing_columns:
            model_column = model_columns.get(column['name'])
            if model_column is None:
                return True
            if column['type'] != str(model_column.type):
                return True
    return False

#checks if the database is empty
def is_db_empty():
    for table in db.Model.metadata.tables.values():
        result = db.session.execute(select(table)).fetchone()
        if result:
            return False
    return True

#use the sql script to populate the database
def populate_db():
    script = os.path.join(os.path.dirname(__file__), 'populate.sql')
    with open(script, 'r') as f:
        sql = f.read()
    db.session.execute(text(sql))
    db.session.commit()

#initializes the database, if the tables in the database are different from the ones in the models, it drops the tables and creates new ones
#also populates the database with some data if it is empty
def init_db():
    with app.app_context():
        if check_db():
            db.drop_all()
            db.create_all()
        if is_db_empty():
            populate_db()

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
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), default = 1)
    title=db.Column(db.String(100))
    year_finished=db.Column(db.Integer)
    cost=db.Column(db.Float)
    period=db.Column(db.String(200))
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

class users(db.Model):
    user_id=db.Column(db.Integer, primary_key=True)
    user_fname=db.Column(db.String(100))
    user_lname=db.Column(db.String(100))
    email=db.Column(db.String(100), unique=True)
    password=db.Column(db.String(100))
    role=db.Column(db.String(1))

class transaction(db.Model):
    transaction_id=db.Column(db.Integer, primary_key=True)
    piece_id = db.Column(db.Integer, db.ForeignKey('art_piece.piece_id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
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