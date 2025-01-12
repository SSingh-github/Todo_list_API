from flask import Flask
from dotenv import load_dotenv
import os
from app import constants
from .routes import main

# Load environment variables from the .env file
load_dotenv()
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy instance
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = constants.Database.TABLE_NAME_USERS

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)



class Task(db.Model):
    __tablename__ = 'tasks'  # Table name in the database

    # Columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(150), nullable=False)  # Task name
    details = db.Column(db.Text, nullable=True)  # Task details (optional)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Date when the task was created
    status = db.Column(db.String(50), default="pending")  # Status of the task (e.g., pending, completed)
    
    # Foreign Key: Link to the user who created the task
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    user = db.relationship('User', backref='tasks', lazy=True)  # Relationship with the User model

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = constants.AppConfig.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = constants.Database.URI_TEMPLATE.format(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    dbname=os.getenv('DB_NAME')
)
app.register_blueprint(main)
db.init_app(app)

# Create the tables in the database if not already created
with app.app_context():
    db.create_all()

# create tables for user and tasks (done)
# create login and signup apis after studying them with proper status codes and unit tests 
