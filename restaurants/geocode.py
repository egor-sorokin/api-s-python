import httplib2
import json


google_api_key = 'AIzaSyCQe4BASdsAFJ1yWLARuKuHL2uuJzQ3GhM'


def getGeocodeLocation(placeName):
    locationString = placeName.replace(' ', '+')
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (locationString, google_api_key))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return latitude, longitude
