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
Our application starts by greeting the user with a login page. Here is the login information that both Professor Wade and TA 