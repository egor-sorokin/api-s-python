import sys
import codecs
from models import Base, Restaurant
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
                                    restaurant_image=unicode(restaurant_info['image']))
            session.add(restaurant)
            session.commit()
            return jsonify(restaurant=restaurant.serialize)

        else:
            return jsonify({"error": "No Restaurants Found for %s in %s" % (meal_type, location)})


@app.route('/restaurants/<int:id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def restaurant_handler(id):
    if request.method == 'GET':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
