from flask import Flask, jsonify, abort, request, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Bagel, User
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

engine = create_engine('sqlite:///bagelShop.db')
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
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        print "Arguments are missed"
        abort(400)

    if session.query(User).filter_by(username=username).first() is not None:
        print "User already exists"
        user = session.query(User).filter_by(username=username).first()
        return jsonify({'message': 'user already exists'}), 200

    user = User(username=username)
    user.hash_password(password)
    session.add(user)
    session.commit()

    return jsonify({'username': user.username}), 201


@app.route('/bagels/', methods=['GET', 'POST'], strict_slashes=False)
@auth.login_required
def showAllBagels():
    if request.method == 'GET':
        bagels = session.query(Bagel).all()
        return jsonify(bagels=[bagel.serialize for bagel in bagels])
    elif request.method == 'POST':
        name = request.json.get('name')
        description = request.json.get('description')
        picture = request.json.get('picture')
        price = request.json.get('price')
        newBagel = Bagel(name=name, description=description, picture=picture, price=price)
        session.add(newBagel)
        session.commit()
        return jsonify(newBagel.serialize)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
