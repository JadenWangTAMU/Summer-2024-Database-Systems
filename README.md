# CSCE 310 Summer 2024 Database Systems Project (The Artfolio Gallery Application)

## If everyhing goes well...
Our application is hosted in the cloud using Heroku. You can access it by clicking [here](https://csce-310-artfolio-8885d6fafd86.herokuapp.com/).

If for some reason the link is not working, you can follow the instructions below to run the application locally.

## Requirements
- Python 3.8 or higher
- Flask
- SQLAlchemy
- Flask-SQLAlchemy
- psycopg2-binary
- PostgresSQL 16 or higher

## External Dependencies
- Tembo (used to host a Postgres database in the cloud) (https://tembo.io/)
- Heroku (used to host the application) (https://www.heroku.com/)
- Github (used to host the code) (https://www.github.com/)

## Installation
Download the application code from Github using command:

`git clone https://github.com/JadenWangTAMU/Summer-2024-Database-Systems.git`

or

`git clone https://github.com/JadenWangTAMU/Summer-2024-Database-Systems/`

## Execute code
Run these commands in the terminal:

### Get all the dependencies
1. Create a virtual environment (name it whatever you want)
`python3 -m venv {name of virtual environment}`

2. Activate the virtual environment (for Mac/Linux)
`source {name of virtual environment}/bin/activate`

  if you are using Windows, use this command instead:

  `source {name of virtual environment}/Scripts/activate`

3. Install the dependencies
`pip install -r requirements.txt`

### Run the application
Enter the following command in the terminal to run the application:
`flask run`

In the terminal, you should see a message that states the application is running on a local server. Copy the link and paste it into your browser to view the application.

![Flask Message](/static/images/readme_image1.png)

## Application Usage
Our application starts by greeting the user with a login page. Here is the login information that both Professor Wade and TA Bengali can use to log in:

- Professor Wade
  - Email: paulinewade@tamu.edu
  - Password: password

- TA Bengali
  - Email: vendangibengali@tamu.edu
  - Password: password

These pieces of login information are used purely to model the behavior of a user logging in. The application will not store any information associated with your email and will not use it for any purpose other than to log you in.

After logging in, the user will be taken to the main page of the application. From here, the application is pretty self-explanatory. Since both Professor Wade and TA Bengali have the same admin permissions, you have access to CRUD operations for all the entites in our application. You can create, read, update, and delete artworks, creators, users, and transactions.

Here is showcasing of the main page of the application:
![Main Page](/static/images/readme_image2.png)

An added feature of our application is the ability to buy paintings. You can click the "Buy A Painting" button on the bottom of the main page and view all sellable paintings. You can click on the "Buy" button to purchase a painting. A transaction will automatically be created and pushed to the database detailing who bought the painting from who at what time.

Here is showcasing of the buy paintings page:
![Buy Paintings](/static/images/readme_image3.png)



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

## Entity Specifications
### Art Piece
An art piece has the following attributes:
- ID (Primary Key) (auto-incremented)
  - Type: Integer (serial)
- Owner ID (Foreign Key) (gotten from the User entity, default is 1 which is the ID of the Artfolio Gallery)
  - Type: Integer
- Creator ID (Foreign Key) (gotten from the Creator entity)
  - Type: Integer
- Title
  - Type: String (100 characters)
- Year finished
  - Type: Integer
- Cost
  - Type: Float
- Period (small description of the period the art piece was created in)
  - Type: String (200 characters)
- Photo link (link to the photo of the art piece)
  - Type: String (1000 characters)
- Sellable (boolean value that determines if the art piece is sellable)
  - Type: Boolean
- Viewable (boolean value that determines if the art piece is viewable)
  - Type: Boolean

### Creator

### User

### Transaction