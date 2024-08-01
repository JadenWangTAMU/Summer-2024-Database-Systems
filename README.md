# CSCE 310 Summer 2024 Database Systems Project (The Artfolio Gallery Application)

## If everyhing goes well...
Our application is hosted in the cloud using Heroku. You can access it by clicking [here](https://csce-310-artfolio-8885d6fafd86.herokuapp.com/).

If for some reason the link is not working, you can follow the instructions below to run the application locally.

## Requirements
- The only requirements that someone will need to run this application is Python 3.8 or higher and git. You can download Python from [here](https://www.python.org/downloads/) and git from [here](https://git-scm.com/downloads).
  - There are external libraries that are used in this application. However, further in the README, there are instructions on how to install all these dependencies. 

## Useful Technologies used to develop the application (NOT NEEDED TO RUN THE APPLICATION)
- Tembo (used to host a Postgres database in the cloud) (https://tembo.io/)
- Heroku (used to host the application) (https://www.heroku.com/)
- Github (used to host the code and version control) (https://www.github.com/)

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

(Within the requirements.txt file, there are all the dependencies that are needed to run the application. Running the command above will install all these dependencies.)

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

## Entity Specifications

### ERD (Entity Relationship Diagram)
![ERD](/static/images/ERD.jpg)



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

#### Create
- A user can create an art piece by filling out all the attributes of the art piece with the exception of the ID since it is auto-incremented. The creator ID is inserted by selecting the creator's name from a dropdown list of all creators in the database. The owner ID is set to 1 by default since the Artfolio Gallery owns all the art pieces.

#### Read
#### Update
#### Delete

### Creator
A creator has the following attributes:
- ID (Primary Key) (auto-incremented)
  - Type: Integer (serial)
- Creator First Name
  - Type: String
- Creator Last Name
  - Type: String
- Birth Country
  - Type: String
- Birth Date
  - Type: Datetime
- Death Date
  - Type: Datetime
#### Create
#### Read
#### Update
#### Delete

### User
A user has the following attributes:
- ID (Primary Key) (auto-incremented)
  - Type: Integer (serial)
- User First Name
  - Type: String
- User Last Name
  - Type: String
- Email (must be unique for all users)
  - Type: String
- Password
  - Type: String
- Role (1 character long)
  - Type: String
#### Create
#### Read
#### Update
#### Delete

### Transaction
A transaction has the following attributes:
- ID (Primary Key) (auto-incremented)
  - Type: Integer (serial)
- Piece ID (Foreign Key) (gotten from the Art Piece entity)
  - Type: Integer
- Buyer ID (Foreign Key) (gotten from the User entity)
  - Type: Integer
- Seller ID (Foreign Key) (gotten from the User entity)
  - Type: Integer
- Timestamp (date where the transaction takes place)
  - Type: Datetime
#### Create
#### Read
#### Update
#### Delete
