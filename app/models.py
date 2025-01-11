from . import db
import constants

class User(db.Model):
    __tablename__ = constants.Database.TABLE_NAME_USERS

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
