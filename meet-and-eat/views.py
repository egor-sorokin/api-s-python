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
def meet_requests_handler():
    if request.method == 'GET':
        meet_requests = session.query(Request).all()
        return jsonify(meet_requests=[i.serialize for i in meet_requests])
    elif request.method == 'POST':
        user_id = request.json.get('user_id')
        meal_type = request.json.get('meal_type')
        location_string = request.json.get('location_string')
        latitude = request.json.get('latitude')
        longitude = request.json.get('longitude')
        meal_time = request.json.get('meal_time')
        filled = request.json.get('filled')

        if session.query(Request).filter_by(user_id=user_id, meal_time=meal_time).first() is not None:
            print "You already have a meet request in that time, please choose another one"
            return jsonify({'message': 'You already have a meet request in that time, please choose another time'}), 200

        new_meet_request = Request(meal_type=meal_type, location_string=location_string, latitude=latitude,
                                   longitude=longitude, meal_time=meal_time, filled=filled, user_id=user_id)
        session.add(new_meet_request)
        session.commit()
        return jsonify(meet_request=new_meet_request.serialize)


@app.route('/api/v1/requests/<int:request_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def meet_request_handler(request_id):
    meet_request = session.query(Request).filter_by(request_id=request_id).one()
    if request.method == 'GET':
        return jsonify(meet_request=meet_request.serialize)
    elif request.method == 'PUT':
        meal_type = request.json.get('meal_type')
        location_string = request.json.get('location_string')
        latitude = request.json.get('latitude')
        longitude = request.json.get('longitude')
        meal_time = request.json.get('meal_time')

        if meal_type:
            meet_request.meal_type = meal_type
        if location_string:
            meet_request.location_string = location_string
        if latitude:
            meet_request.latitude = latitude
        if longitude:
            meet_request.longitude = longitude
        if meal_time:
            meet_request.meal_time = meal_time

        session.add(meet_request)
        session.commit()

        return jsonify(meet_request=meet_request.serialize)
    elif request.method == 'DELETE':
        session.delete(meet_request)
        session.commit()
        print "Removed the meet request with id %s" % request_id
        return jsonify({'message': 'The meet request has been successfully removed'}), 200


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
