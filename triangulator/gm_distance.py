# pip install googlemaps
import triangulator.keys as keys
import googlemaps

# Requires API key
gmaps = googlemaps.Client(key=keys.get_google_maps_key())


def getDistance(dest: str, starting: str) -> str:
    my_dist = gmaps.distance_matrix(dest, starting)['rows'][0]['elements'][0]
    return my_dist['duration']['text']
