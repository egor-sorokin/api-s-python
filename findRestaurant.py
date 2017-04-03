import json
import httplib2
import sys
import codecs
from geocode import getGeocodeLocation

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = 'PQ10XH5TCF5MLEZW51XYJVN24ODIL3IIWXXAUI2CA1HUGRWD'
foursquare_client_secret = '4BFTG00AFBDPLCXEDLY4F15VKJBQFON5X0RDMAXAHDOGNXAU'


def find_restaurant(meal_type, location):
    lat, lng = getGeocodeLocation(location)
    url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s' % (
        foursquare_client_id, foursquare_client_secret, lat, lng, meal_type))

    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    response = result['response']['venues']

    if response:
        restaurant = response[0]
        restaurant_name = restaurant['name']
        restaurant_address = restaurant['location']['formattedAddress']
        address = ''
        for i in restaurant_address:
            address += i + " "
        restaurant_address = address

        venue_id = restaurant['id']
        url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % (
            (venue_id, foursquare_client_id, foursquare_client_secret)))
        result = json.loads(h.request(url, 'GET')[1])
        photos = result['response']['photos']['items']

        if photos:
            photo = photos[0]
            suffix = photo['suffix']
            prefix = photo['prefix']
            image_url = prefix + '300x300' + suffix
        else:
            image_url = 'https://resizer.otstatic.com/v2/photos/medium/23668132.jpg'

        restaurant_info = {'name': restaurant_name, 'address': restaurant_address, 'image': image_url}
        print "Restaurant: %s" % restaurant_info['name']
        print "Address: %s" % restaurant_info['address']
        print "Image: %s \n" % restaurant_info['image']

        return restaurant_info
    else:
        print "No venues founded in %s" % location
        return "No restaurants founded"

if __name__ == '__main__':
    find_restaurant("Pizza", "Tokyo, Japan")
    find_restaurant("Sushi", "Omsk, Russia")
    find_restaurant("Tacos", "Jakarta, Indonesia")
    find_restaurant("Spaghetti", "New Delhi, India")
    find_restaurant("Sushi", "Los Angeles, California")
    find_restaurant("Gyros", "Sydney Australia")
