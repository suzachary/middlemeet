# need to perform geocoding
# 'pip install geopy' from command prompt

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="hike_triangulator")


# to calculate midpoint between 2+ locations,
# add all the latitudes and divide by the number of latitudes given (x-coord)
# add all the longitudes and divide by the number of longitudes given (y-coord)

# midpoint calculation
# INPUT FROM FRONTEND: LIST OF STRINGS OF ADDRESSES

def get_midpoint(addresses: [str]) -> (int, int):  # <-- called from frontend
    lats = []
    longs = []
    for address in addresses:
        location = geolocator.geocode(address)
        lats.append(location.latitude)
        longs.append(location.longitude)

    return calculate_midpoint(lats, longs)


def calculate_midpoint(lats: list, longs: list) -> (int, int):
    lat_avg = sum(lats) / len(lats)
    long_avg = sum(longs) / len(longs)
    return lat_avg, long_avg

