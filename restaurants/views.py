import os, sys
import codecs
from models import Base, Restaurant
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from findRestaurant import find_restaurant


sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)
engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine

DBsession = sessionmaker(bind=engine)
session = DBsession()

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/', methods=['GET', 'POST'], strict_slashes=False)
def all_restaurants_handler():
    if request.method == 'GET':
        restaurants = session.query(Restaurant).all()
        return jsonify(restaurants=[i.serialize for i in restaurants])

    elif request.method == 'POST':
        location = request.args.get('location', '')
        meal_type = request.args.get('mealType', '')
        restaurant_info = find_restaurant(meal_type, location)
        if restaurant_info != 'No restaurants founded':
            restaurant = Restaurant(restaurant_name=unicode(restaurant_info['name']),
                                    restaurant_address=unicode(restaurant_info['address']),
                                    restaurant_image=restaurant_info['image'])
            session.add(restaurant)
            session.commit()
            return jsonify(restaurant=restaurant.serialize)

        else:
            return jsonify({"error": "No Restaurants Found for %s in %s" % (meal_type, location)})


@app.route('/restaurants/<int:id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def restaurant_handler(id):
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    if request.method == 'GET':
        return jsonify(restaurant=restaurant.serialize)

    elif request.method == 'PUT':
        address = request.args.get('address', '')
        name = request.args.get('name', '')
        image = request.args.get('image', '')

        if address:
            restaurant.restaurant_address = address
        if name:
            restaurant.restaurant_name = name
        if image:
            restaurant.restaurant_image = image

        session.add(restaurant)
        session.commit()

        return jsonify(restaurant=restaurant.serialize)

    elif request.method == 'DELETE':
        session.delete(restaurant)
        session.commit()

        return 'Successfully deleted'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
