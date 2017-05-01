import json
import httplib2
import requests

from flask import Flask, jsonify, request, g, render_template, abort, make_response
from flask.ext.httpauth import HTTPBasicAuth
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

auth = HTTPBasicAuth()
engine = create_engine('sqlite:///paleKale.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']


@auth.verify_password
def verify_password(userame_or_token, password):
    user_id = User.verify_auth_token(userame_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
    else:
        user = session.query(User).filter_by(username=userame_or_token).first()
        if not user or not verify_password(password):
            return False

    g.user = user
    return True


@app.route('/clientOAuth/', strict_slashes=True)
def start():
    return render_template('clientOAuth.html')


@app.route('/oauth/<provider>/', methods=['POST'], strict_slashes=False)
def login(provider):
    auth_code = request.json.get('auth_code')
    print "Step 1 - Complete, received auth code %s" % auth_code
    if provider == 'google':
        # Token exchanging
        try:
            # Upgrade the authorization code into a credentials object
            oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(auth_code)
        except FlowExchangeError:
            response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Check that the access token is valid.
        access_token = credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])
        # If there was an error in the access token info, abort.
        if result.get('error') is not None:
            response = make_response(json.dumps(result.get('error')), 500)
            response.headers['Content-Type'] = 'application/json'

        print "Step 2 Complete! Access Token : %s " % credentials.access_token

        # Find user or make a new one
        h = httplib2.Http()
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)

        data = answer.json()

        name = data['name']
        picture = data['picture']
        email = data['email']

        # see if user exists, if it doesn't make a new one
        user = session.query(User).filter_by(email=email).first()
        if not user:
            user = User(username=name, picture=picture, email=email)
            session.add(user)
            session.commit()

        # Make token
        token = user.generate_auth_token(600)

        # Send back token to the client
        return jsonify({'token': token.decode('ascii')})
    else:
        return 'Unrecoginized Provider'


@app.route('/token/', strict_slashes=False)
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route('/users/', methods=['POST'], strict_slashes=True)
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        print "Arguments were missed"
        abort(400)

    if session.query(User).filter_by(username=username).first() is not None:
        print "User already exists"
        return jsonify({'message': 'user already exists'}), 200

    user = User(username=username)
    user.password_hash(password)
    session.add(user)
    session.commit()


@app.route('/api/resource/', methods=['GET'], strict_slashes=False)
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


if __name__ == '__main__':
    app.debug = True
    # for the local environment use localhost:5000 in your browser
    app.run(host='localhost', port=5000)
