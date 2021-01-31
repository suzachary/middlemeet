# Sending user a text to their phone(s) for the selected activities address
# npm install twilio-cli -g
# pip install twilio
# Download the helper library from https://www.twilio.com/docs/python/install

import triangulator.keys as keys
from twilio.rest import Client

account_sid = keys.get_twilio_SID()
auth_token = keys.get_twilio_auth()
client = Client(account_sid, auth_token)


def sendText(message, reciever):  # <-- called from frontend
    message = client.messages \
        .create(
        body=message,
        from_='+19492697262',
        to=reciever or '+14087724552'
    )
    print(message.sid)
