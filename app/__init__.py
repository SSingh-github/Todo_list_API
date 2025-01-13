from flask import Flask, request, jsonify, session
from dotenv import load_dotenv
import os
from app import constants
from .routes import main
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from datetime import datetime
import secrets
from flask_sqlalchemy import SQLAlchemy


# Load environment variables from the .env file
load_dotenv()

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
app.secret_key = secrets.token_hex(32)

# Configure session security
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.register_blueprint(main)
db.init_app(app)

# Create the tables in the database if not already created
with app.app_context():
    db.create_all()

# create tables for user and tasks (done)
# create login and signup apis after studying them with proper status codes and unit tests 

@app.route('/signup', methods=['POST'])
def signup():
    try:
        # Parse the JSON payload
        data = request.get_json()

        if not data:
            return jsonify({'message': 'No data provided'}), 400  # Bad Request
        
        username = data.get('username')
        password = data.get('password')

        # Validate input
        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400  # Bad Request

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'Username already exists'}), 409  # Conflict

        # Hash the password
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Create a new user entry
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201  # Created

    except Exception as e:
        db.session.rollback()  # Roll back in case of error
        print(f"Error occurred: {e}")
        return jsonify({'message': f'Internal Server Error{e}'}), 500  # Internal Server Error


@app.route('/login', methods=['POST'])
def login():
    try:
        # Parse the JSON payload
        data = request.get_json()

        if not data:
            return jsonify({'message': 'No data provided'}), 400  # Bad Request

        username = data.get('username')
        password = data.get('password')

        # Validate input
        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400  # Bad Request

        # Check if the user exists
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404  # Not Found

        # Verify the password
        if not check_password_hash(user.password, password):
            return jsonify({'message': 'Incorrect password'}), 401  # Unauthorized

        session['user_id'] = user.id
        session['username'] = user.username

        return jsonify({'message': 'Login successful', 'user_id': user.id}), 200  # OK

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500  # Internal Server Error


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function
    
@app.route('/protected', methods=['GET'])
@login_required
def protected():
    return jsonify({'message': f'Welcome, {session["username"]}'}), 200

