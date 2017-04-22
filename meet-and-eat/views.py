import string
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, g, request, jsonify, abort
from models import Base, User, MeetRequest, Proposal, MealDate
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


@app.route('/api/v1/users/', methods=['GET', 'POST'], strict_slashes=False)
def users_handler():
    if request.method == 'GET':
        try:
            users = session.query(User).all()
            return jsonify(users=[i.serialize for i in users]), 200
        except ValueError:
            print "Users are not found, database is empty"
            abort(400)

    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        if username is None or password is None:
            print "Arguments are missed"
            abort(400)

        if session.query(User).filter_by(username=username).first() is not None:
            print "User already exists"
            return jsonify({'message': 'user already exists'}), 200

        user = User(username=username)
        user.hash_password(password)
        session.add(user)
        session.commit()

        return jsonify(user=user.serialize), 201


@app.route('/api/v1/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def user_handler(user_id):
    try:
        user = session.query(User).filter_by(id=user_id).one()
        if request.method == 'GET':
            return jsonify(user.serialize), 200
        elif request.method == 'PUT':
            username = request.json.get('username')

            if username is not None:
                user.username = username
                session.add(user)
                session.commit()
                return jsonify(user=user.serialize)
            else:
                print "Arguments are missed"
                abort(400)

        elif request.method == 'DELETE':
            session.delete(user)
            session.commit()
            return jsonify({'message': 'user was successfully deleted'}), 200
    except ValueError:
        print "User is not found, incorrect user_id"
        abort(400)


@app.route('/api/v1/requests/', methods=['POST', 'GET'], strict_slashes=False)
def meet_requests_handler():
    pass


@app.route('/api/v1/requests/<int:id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def meet_request_handler(id):
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
