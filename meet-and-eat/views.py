import string
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, g, request, jsonify, abort
from models import Base, User, Request, Proposal, MealDate
from flask.ext.httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()
engine = create_engine('sqlite:///meetandeat.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@auth.verify_password
def verify_password(username_or_token, password):
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
    else:
        user = session.query(User).filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False

    g.user = user
    return True


@app.route('/token/', strict_slashes=False)
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route('/api/v1/<string:provider>/login', methods=['POST'], strict_slashes=False)
def login(provider):
    pass


@app.route('/api/v1/<string:provider>/logout', methods=['POST'], strict_slashes=False)
def logout(provider):
    pass


@app.route('/api/v1/users/', methods=['POST', 'GET', 'PUT', 'DELETE'], strict_slashes=False)
def users_handler():
    pass


@app.route('/api/v1/users/<int:id>', methods=['GET'], strict_slashes=False)
def user_handler(id):
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
