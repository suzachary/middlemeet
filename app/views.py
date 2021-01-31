from flask import render_template, request, url_for
from app import app

from triangulator.midpoint import get_midpoint
from triangulator.yelp import getListOfLocations
from triangulator.gm_distance import getDistance
from triangulator.send_sms import sendText

# utility functions
def make_location(*location_parts):
    return (' '.join(location_parts)).strip()

def get_locations(result_dict):
    locations = []
    people = len(result_dict) // 4

    for person in range(1, people + 1):
        street = result_dict[f"street{person}"]
        city = result_dict[f"city{person}"]
        state = result_dict[f"state{person}"]
        zip_code = result_dict[f"zip{person}"]

        full_location = make_location(street, city, state, zip_code)
        locations.append(full_location)
    
    return locations

# route for home page with user input
@app.route('/')
def user_input():
    return render_template('userinput.html', title='User Input')

# route for output page
@app.route('/results', methods=['GET', 'POST'])
def user_output():
    # get form results
    user_input_dict = request.form
    # print(user_input_dict)

    # parse into locations
    locations = get_locations(user_input_dict)
    # print(locations)

    # testing midpoint
    lat, long = get_midpoint(locations)
    print(f'lat: {lat} long: {long}')

    # get other information
    activity = user_input_dict['activity']
    # print(activity)

    phone_no = user_input_dict['phone']
    # print(phone_no)

    max_results = user_input_dict['maxres']

    # get results
    yelp_data = getListOfLocations(
        term=activity,
        lat=lat,
        long=long,
        limit=max_results
    )

    # get estimated times for travel
    for activity_info in yelp_data:
        activity_location = activity_info['location']

        times = []
        for address in locations:
            time_str = getDistance(activity_location, address)
            times.append(f'Estimated time of travel for {address.upper()} is {time_str}')

        activity_info["times"] = times

    # add an ID
    for index, activity_info in enumerate(yelp_data):
        activity_info['divid'] = f"activity{index}"

    # DEBUG
    print(f'user input: {user_input_dict}')
    print(yelp_data)

    return render_template('useroutput.html', title='User Output', yelp_data=yelp_data, phone_no=phone_no)

@app.route('/twilio/<phone_no>/<name>/<address>')
def twilio(phone_no, name, address):
    # rebind phone number with +1
    phone_no = f"+1{phone_no}"

    # run twilio things
    print('twilio function')

    print(f'phone number {phone_no}')
    print(f'business name {name}')
    print(f'address {address}')
    

    # send the text
    msg_text = f"The address of your chosen location is {address}."
    print(f'msg_text: {msg_text}')
    print(f'phone number: {phone_no}')

    sendText(msg_text, phone_no)

    return render_template('twilio.html', phone_no=phone_no, name=name, address=address)