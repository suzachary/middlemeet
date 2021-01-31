import yelp
import send_sms
import midpoint
 #FOR TESTING ONLY RIGHT NOW
if __name__ == "__main__":
    info = {
        'term': 'Food',
        'latitude': 33.64925107405803,
        'longitude': -117.83492869557854,
        'limit': 5,
        'radius': 25000
    }
    
    print(yelp.getLocations(info))



