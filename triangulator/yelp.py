# Getting results from Yelp API

import triangulator.keys as keys

import argparse
import requests
import sys

from urllib.error import HTTPError
from urllib.parse import quote

# API constants
API_KEY = keys.get_yelp_key()
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'


# Defaults for our simple example.
# Have the user select them
# DEFAULT_TERM = 'Food'


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        api_key (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location, info):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    """
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    """
    return request(API_HOST, SEARCH_PATH, api_key, url_params=info)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, api_key)


def query_api(term, location, info):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location, info)
    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    return businesses


def findLocations(info):
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term',
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        return query_api(input_values.term, input_values.location, info)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


# Must pass the info as a dict with parameter values changed to desired values:
# info = {
#         'term': 'food', # <--- string of business/location type
#         'latitude': 33.64925107405803, # <--- latititude of meetup location
#         'longitude': -117.83492869557854, # <---- longitude of meetup location
#         'limit': 5, # <---- number of locations you want included in list
#         'radius': 500 # <---- radius in meters
#     }


def setInfo(term, lat, long, limit, radius = 5000):
    info = dict()
    info['term'] = term
    info['latitude'] = lat
    info['longitude'] = long
    info['limit'] = limit
    # info['radius'] = radius
    return info


def buildLocationList(info):
    all_businesses = findLocations(info)
    business_list = list()
    for business in all_businesses:
        business_dict = dict()
        business_dict["name"] = business["name"]
        business_dict["image_url"] = business["image_url"]
        business_dict["business_url"] = business["url"]
        business_dict["location"] = ", ".join(business["location"]["display_address"])
        business_dict["rating"] = business["rating"]

        business_list.append(business_dict)

    business_list = sorted(business_list, key=lambda i: i['rating'], reverse=True)
    return business_list


def getListOfLocations(term: str, lat: float, long: float, limit: int):  # <-- called from the frontend
    info = setInfo(term, lat, long, int(limit))
    business_list = buildLocationList(info)
    if business_list == None:
        return list({"name": "NONE", "image_url": "https://emojis.wiki/emoji-pics/apple/man-gesturing-no-apple.png", "business_url": "google.com", "location": "NONE", "rating" : 0.0})
    return business_list
