from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from . import constants
from .routes import main

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
app.register_blueprint(main)
db = SQLAlchemy(app)


# Create the tables in the database
with app.app_context():
    db.create_all()
