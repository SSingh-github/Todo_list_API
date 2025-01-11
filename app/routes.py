from flask import Blueprint, jsonify
from . import constants

# Define a blueprint for routes
main = Blueprint('main', __name__)

@main.route('/')
def hello():
    return constants.Messages.HELLO_WORLD