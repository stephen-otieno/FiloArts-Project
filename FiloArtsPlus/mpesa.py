import json
import base64
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth


class Credentials:
    consumer_key = "mqWppb4p80sGJL5elZiFrnsH8SxZFSccpk4XC2GL87ItYmVd"
    consumer_secret = "vZhFfQy4vGcUN41VYDF1msW2TU9wl7GbSsKD1uwNCGaiAfd7cXNbHA3H243DKfF8"
    # passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    api_url ="https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"




class AccessToken:
    request = requests.get(Credentials.api_url, auth=HTTPBasicAuth(Credentials.consumer_key, Credentials.consumer_secret))
    access_token = json.loads(request.text)['access_token']


class Password:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    shortcode = "174379"
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    # passkey = Credentials.passkey
    to_encode = shortcode + passkey +timestamp
    encoded_password = base64.b64encode(to_encode.encode())
    encode_str = shortcode + passkey +timestamp
    decoded_password = encoded_password.decode('utf-8')

    # encoded = base64.b64encode(encode_str.encode())
