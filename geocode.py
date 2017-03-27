import httplib2
import json


def getGeocodeLocation(placeName):
    google_api_key = 'AIzaSyCQe4BASdsAFJ1yWLARuKuHL2uuJzQ3GhM'
    locationString = placeName.replace(' ', '+')
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (locationString, google_api_key))
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)
    return result
