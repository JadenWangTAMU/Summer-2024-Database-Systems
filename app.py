from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, inspect, text
from sqlalchemy.types import Integer, String, VARCHAR, Float, DateTime
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import pytz
import os
import psycopg2

type_mapping = {
    Integer: 'integer',
    String: 'varchar',
    VARCHAR: 'varchar',
    Float: 'double_precision',
    DateTime: 'timestamp'
}


#checks if tables in the database are different from the ones in the models
def check_db():
    #get the tables in the database and the models
    insepector = inspect(db.engine)
    existing_tables = insepector.get_table_names()
    model_tables = db.Model.metadata.tables.keys()
    #checking if the tables in the database are different from the ones in the models
    if set(existing_tables) != set(model_tables):
        return True
    #checking if the columns in the tables in the database are different from the ones in the models
    for table_name in model_tables:
        existing_columns = insepector.get_columns(table_name)
        model_columns = db.Model.metadata.tables[table_name].columns

        if len(existing_columns) != len(model_columns):
            return True
        
        for column in existing_columns:
            model_column = model_columns.get(column['name'])
            if model_column is None:
                print('Column', column['name'], 'does not exist in table', table_name)
                return True
            
            existing_column_type = type(column['type']).__name__.lower()
            model_column_type = type(model_column.type).__name__.lower()

            existing_column_type = type_mapping.get(type(column['type']), existing_column_type)
            model_column_type = type_mapping.get(type(model_column.type), model_column_type)

            if existing_column_type != model_column_type:
                print('Type mismatch for column', column['name'], 'in table', table_name)
                print('Existing column type:', existing_column_type)
                print('Model column type:', model_column_type)
                return True

    #if the tables and columns are the same, return False
    return False

#checks if the database is empty
def is_db_empty():
    #get all the tables in the database
    for table in db.Model.metadata.tables.values():
        #select all from the table
        result = db.session.execute(select(table)).fetchone()
        #if result is not None, the table is not empty
        if result:
            return False
    #if all tables are empty, return True
    return True

#use the sql script to populate the database
def populate_db():
    #get the sql script
    script = os.path.join(os.path.dirname(__file__), 'populate.sql')
    #execute the sql script
    with open(script, 'r') as f:
        sql = f.read()
    db.session.execute(text(sql))
    #commit the changes to the database
    db.session.commit()

#initializes the database, if the tables in the database are different from the ones in the models, it drops the tables and creates new ones
#also populates the database with some data if it is empty
def init_db():
    with app.app_context():
        #if the tables in the database are different from the ones in the models, drop the tables and create new ones
        if check_db():
            print("Database schema does not match the models, dropping current tables")
            db.drop_all()
            print("Creating new tables in accordance with the models")
            db.create_all()
        #if the database is empty, populate it with data from the sql script
        if is_db_empty():
            print("Database is empty, populating with data from sql script")
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
    timestamp=db.Column(db.DateTime, default= lambda: datetime.now(pytz.timezone('US/Central')))

init_db()

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        #get the email and password from the form
        email = request.form['email']
        password = request.form['password']

        #find the user with the inputted email in the database
        user = users.query.filter_by(email=email).first()
        #if the user exists and the password is correct, log them in
        if user and user.password == password:
            flash('You have been logged in', 'success')
            session["user_email"] = email
            session["user_password"] = password
            return redirect(url_for('buy_menu'))
        else:
            #if the user does not exist or the password is incorrect, flash an error message
            flash('Invalid email or password', 'danger')
            return render_template("index.html")
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
        #else just get all the paintings that are viewable
        paintings_query = art_piece.query.filter(art_piece.viewable == True)
    
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

@app.route('/buy_menu', methods = ['GET'])
def buy_menu():
    #used for page stuff
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '', type=str)
    sort_by = request.args.get('sort_by', 'title', type=str)
    #can change this to whatever, decides how many paintings are shown per page
    per_page = 5

    # does the user want to search for a painting?
    if query:
        #filter based on what they searched for
        paintings_query = art_piece.query.filter(art_piece.title.ilike(f'%{query}%'), art_piece.sellable == True)
    else:
        #else just get all the paintings that are sellable
        paintings_query = art_piece.query.filter(art_piece.sellable == True)
    
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
    return render_template("buy_menu.html", paintings = paintings.items, creators = all_creators, pagination = paintings, query=query, sort_by = sort_by)

@app.route('/buy_painting/<int:piece_id>', methods = ['POST'])
def buy_painting(piece_id):
    # TODO: ask the user once they buy a painting if they want to keep it in the gallery. If not then viewable will be set to false and the painting will then have the requirements to be deleted from the database (sellable & viewable = false means the painting should be deleted)
    #might tweak this later
    buyer_email = session.get("user_email")
    if not buyer_email:
        flash('You must be logged in to buy a painting', 'danger')
        return redirect(url_for('index'))
    
    buyer = users.query.filter_by(email=buyer_email).first()
    if not buyer:
        flash('User not found', 'danger')
        return redirect(url_for('index'))
    
    painting = art_piece.query.get(piece_id)
    if painting and painting.sellable:
        #painting is no longer sellable after being bought
        painting.sellable = False

        #create a transaction for the purchase
        trans = transaction(piece_id=piece_id, buyer_id=buyer.user_id, seller_id=painting.owner_id)

        #change the owner of the painting to the buyer
        painting.owner_id = buyer.user_id
        db.session.add(trans)
        db.session.commit()
        flash(f'Painting "{painting.title}" purchased successfully', 'success')
        return redirect(url_for('buy_menu'))
    else:
        flash('Painting not found or not sellable', 'danger')
        return "Painting not available for purchase", 404

@app.route('/delete_paintings', methods = ['GET', 'POST'])
def delete_paintings():
    if request.method == 'POST':
        #get the id of the painting to delete
        painting_id = request.form['painting_id']
        try:
            #try and delete the painting
            painting = art_piece.query.get(painting_id)
            if painting:
                db.session.delete(painting)
                db.session.commit()
                flash(f'Painting "{painting.title}" deleted successfully', 'success')
            else:
                flash('Painting not found', 'danger')
        except IntegrityError as e:
            #if the painting is referenced in another table, it can't be deleted (foreign key constraint)
            db.session.rollback()
            flash(f'Error deleting painting: This painting is referenced in another table and therefore can not be deleted as to keep foreign key integrity.', 'danger')
        except Exception as e:
            #handle any other unexpected errors
            db.session.rollback()
            flash(f'Error deleting painting: {e}', 'danger')
        #go back to the delete paintings page
        return redirect(url_for('delete_paintings'))
    #get all the paintings
    paintings = art_piece.query.all()
    #render the delete paintings page with all the paintings
    return render_template("delete_paintings.html", paintings = paintings)

@app.route('/create_painting', methods = ['GET', 'POST'])
def create_painting():
    if request.method == 'POST':
        title = request.form.get('title')
        #default owner of the painting is the museum
        owner = 1
        creator_id = request.form.get('creator_id')
        period = request.form.get('period')
        year_finished = request.form.get('year_finished')
        cost = request.form.get('cost')
        photo_link = request.form.get('photo_link')
        sellable = request.form.get('sellable') == 'true'
        viewable = request.form.get('viewable') == 'true'

        if not title or not period or not cost or not photo_link or not year_finished:
            flash('Please fill out all fields', 'danger')
            return redirect(url_for('create_painting'))
    
        new_painting = art_piece(owner_id=owner, creator_id=creator_id, title=title, year_finished=year_finished, period=period, cost=cost, photo_link=photo_link, sellable=sellable, viewable=viewable)

        try:
            db.session.add(new_painting)
            db.session.commit()
            flash(f'Painting "{title}" created successfully', 'success')
            return redirect(url_for('create_painting'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating painting: {e}', 'danger')
            return redirect(url_for('create_painting'))
    creators = creator.query.all()
    return render_template("create_painting.html", creators=creators)


# TODO: rework this, this is bad
@app.route('/update_paintings', methods=['GET', 'POST'])
def update_paintings():
    if request.method == 'POST':
        paintings = art_piece.query.all()
        for painting in paintings:
            title = request.form.get(f'title_{painting.piece_id}')
            period = request.form.get(f'description_{painting.period}')
            price = request.form.get(f'price_{painting.piece_id}')
            sellable = request.form.get(f'sellable_{painting.piece_id}') == 'true'
            viewable = request.form.get(f'viewable_{painting.piece_id}') == 'true'

            if title:
                painting.title = title
            if period:
                painting.description = period
            if price:
                painting.cost = price
            painting.sellable = sellable
            painting.viewable = viewable

        db.session.commit()
        flash('All paintings updated successfully', 'success')
        return redirect(url_for('update_paintings'))

    paintings = art_piece.query.all()
    return render_template('update_paintings.html', paintings=paintings)

# Read creator function for display
def getcreator():
    return creator.query.all()

# Function to get creator names mapped to IDs
def get_creator_names():
    creators = creator.query.all()
    creator_names = {f"{creator.creator_fname} {creator.creator_lname}": creator.creator_id for creator in creators}
    return creator_names

@app.route("/readcreator")
def readcreators():
    try:
        creator_list = getcreator()
        return render_template("r_creator.html", creatorlist=creator_list)
    except Exception as e:
        print("Error in readcreators function:")
        print(e)
        traceback.print_exc()
        return "An error occurred while fetching the creators.", 500

# update creator function to allow modification 
@app.route("/updatecreator")
def updatecreators(feedback_message=None, feedback_type=False):
    creator_names = get_creator_names()
    return render_template("u_creator.html", 
                           creatornames=creator_names.keys(), 
                           feedback_message=feedback_message, 
                           feedback_type=feedback_type)

@app.route("/creatorupdate", methods=['POST'])
def creatorupdate():
    creator_name = request.form.get('creatornames')
    creator_fname = request.form["cfname"]
    creator_lname = request.form["clname"]
    birth_country = request.form["country"]
    birth_date = request.form["bdate"]
    death_date = request.form["ddate"]

    creator_names = get_creator_names()
    creator_id = creator_names.get(creator_name)
    
    if not creator_id:
        return updatecreators(feedback_message=f'Creator {creator_name} not found.', feedback_type=False)
    
    try:
        obj = creator.query.filter_by(creator_id=creator_id).first()
        
        if not obj:
            return updatecreators(feedback_message=f'Creator {creator_name} not found.', feedback_type=False)

        if creator_fname:
            obj.creator_fname = creator_fname
        if creator_lname:
            obj.creator_lname = creator_lname
        if birth_country:
            obj.birth_country = birth_country
        if birth_date:
            obj.birth_date = birth_date
        if death_date:
            obj.death_date = death_date

        db.session.commit()
        return updatecreators(feedback_message=f'Successfully updated creator {creator_name}', feedback_type=True)
    except Exception as err:
        db.session.rollback()
        return updatecreators(feedback_message=str(err), feedback_type=False)

# create creator function 
@app.route("/createcreator")
def createcreator(feedback_message=None, feedback_type=False):
    return render_template("c_creator.html",
            feedback_message=feedback_message, 
            feedback_type=feedback_type)

@app.route("/creatorcreate", methods=['POST'])
def creatorcreate():
    creator_fname = request.form["cfname"]
    creator_lname = request.form["clname"]
    birth_country = request.form["country"]
    birth_date = request.form["bdate"]
    death_date = request.form["ddate"]

    # Check if a creator with the same first name and last name already exists
    existing_creator = db.session.query(creator).filter_by(
        creator_fname=creator_fname, creator_lname=creator_lname).first()

    if existing_creator:
        return createcreator(feedback_message=f'A creator named {creator_fname} {creator_lname} already exists.', feedback_type=False)

    try:
        new_creator = creator(
            creator_fname=creator_fname, 
            creator_lname=creator_lname, 
            birth_country=birth_country, 
            birth_date=birth_date, 
            death_date=death_date
        )
        db.session.add(new_creator)
        db.session.commit()
        return createcreator(feedback_message=f'Successfully added creator {creator_fname} {creator_lname}', feedback_type=True)
    except Exception as err:
        db.session.rollback()
        return createcreator(feedback_message=f'Database error: {err}', feedback_type=False)

# create delete creator function 
@app.route("/deletecreator")
def deletecreator(feedback_message=None, feedback_type=False):
    creator_names = get_creator_names()
    return render_template("d_creator.html", 
                           creatornames=creator_names.keys(), 
                           feedback_message=feedback_message, 
                           feedback_type=feedback_type)

@app.route("/creatordelete", methods=['POST'])
def creatordelete():
    creator_name = request.form.get('creatornames')

    # if not request.form.get('confirmInput'):
    #     return deletecreator(feedback_message='Operation canceled. Creator not deleted.', feedback_type=False)
    
    creator_names = get_creator_names()
    creator_id = creator_names.get(creator_name)

    if not creator_id:
        return deletecreator(feedback_message=f'Creator {creator_name} not found.', feedback_type=False)

    try:
        obj = creator.query.filter_by(creator_id=creator_id).first()
        
        if not obj:
            return deletecreator(feedback_message=f'Creator {creator_name} not found.', feedback_type=False)
        
        # Check if the creator is associated with any art pieces
        associated_art_pieces = db.session.query(art_piece).filter_by(creator_id=creator_id).all()
        if associated_art_pieces:
            return deletecreator(feedback_message=f'Creator {creator_name} is associated with an art piece, and cannot be deleted.', feedback_type=False)

        db.session.delete(obj)
        db.session.commit()
        return deletecreator(feedback_message=f'Successfully deleted creator {creator_name}', feedback_type=True)
    except Exception as err:
        db.session.rollback()
        return deletecreator(feedback_message=f'Database error: {err}', feedback_type=False)
#this is the main function that runs the app
if __name__ == '__main__':
    app.run(debug = True)