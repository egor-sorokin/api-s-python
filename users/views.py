from flask import Flask, jsonify, url_for, abort, request, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User
from sqlalchemy.ext.declarative import declarative_base

from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


engine = create_engine('sqlite:///users.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)


@auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@app.route('/users/', methods=['POST'], strict_slashes=False)
def new_user():
    username = request.args.get('username')
    password = request.args.get('password')

    if username is None or password is None:
        print "missing arguments"
        abort(400)
    if session.query(User).filter_by(username=username).first() is not None:
        print "existing user"
        user = session.query(User).filter_by(username=username).first()
        return jsonify({'message': 'user already exists'}), 200

    user = User(username=username)
    user.hash_password(password)
    session.add(user)
    session.commit()

    return jsonify({'username': user.username}), 201


@app.route('/protected_resource', methods=['GET'])
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
