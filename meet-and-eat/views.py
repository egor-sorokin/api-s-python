import string
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, g, request, jsonify, abort
from models import Base, User, Request, Proposal, MealDate


engine = create_engine('sqlite:///meetandeat.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@app.route('/api/v1/<string:provider>/login', methods=['POST'], strict_slashes=False)
def login(provider):
    pass


@app.route('/api/v1/<string:provider>/logout', methods=['POST'], strict_slashes=False)
def logout(provider):
    pass


@app.route('/api/v1/users/', methods=['POST', 'GET', 'PUT', 'DELETE'], strict_slashes=False)
def users():
    pass


@app.route('/api/v1/users/<int:id>', methods=['GET'], strict_slashes=False)
def user(id):
    pass


@app.route('/api/v1/requests/', methods=['POST', 'GET'], strict_slashes=False)
def requests():
    pass


@app.route('/api/v1/requests/<int:id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def request(id):
    pass


@app.route('/api/v1/proposals/', methods=['POST', 'GET'], strict_slashes=False)
def proposals():
    pass


@app.route('/api/v1/proposals/<int:id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def proposal(id):
    pass


@app.route('/api/v1/dates/', methods=['POST', 'GET'], strict_slashes=False)
def dates():
    pass


@app.route('/api/v1/dates/<int:id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def date(id):
    pass


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
