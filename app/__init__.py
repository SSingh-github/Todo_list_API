from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import constants

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = constants.AppConfig.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = constants.Database.URI_TEMPLATE.format(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    dbname=os.getenv('DB_NAME')
)
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = constants.Database.TABLE_NAME_USERS  # Table name in the database

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    username = db.Column(db.String(150), nullable=False, unique=True)  # Username, must be unique
    password = db.Column(db.String(255), nullable=False)  # Password (hashed for security)

# Create the tables in the database
with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return constants.Messages.HELLO_WORLD