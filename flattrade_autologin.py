import requests
import pyotp
import hashlib
import logging
from urllib.parse import urlparse, parse_qs
from api_helper import NorenApiPy

logging.basicConfig(level=logging.INFO)


USER = "username"
PWD = "password"
TOTP_KEY = "TOTP_key"
API_KEY = "api_key"
API_SECRET = "api_secret"


HOST = "https://auth.flattrade.in"
API_HOST = "https://authapi.flattrade.in"

routes = {
    "session" : f"{API_HOST}/auth/session",
    "ftauth" : f"{API_HOST}/ftauth",
    "apitoken" : f"{API_HOST}/trade/apitoken",
}

headers = {
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Host": "authapi.flattrade.in",
    "Origin": f"{HOST}",
    "Referer": f"{HOST}/",
}

def encode_item(item):
    encoded_item = hashlib.sha256(item.encode()).hexdigest() 
    return encoded_item


def get_authcode():
    response = requests.post(routes["session"], headers= headers)
    if response.status_code == 200:
        sid = response.text
        response =  requests.post(
                routes["ftauth"],
                json = {
                        "UserName": USER,
                        "Password": encode_item(PWD),
                        "App":"",
                        "ClientID":"",
                        "Key":"",
                        "APIKey": API_KEY,
                        "PAN_DOB": pyotp.TOTP(TOTP_KEY).now(),
                        "Sid" : sid,
                        "Override": ""
                        },
                    headers= headers
                    )    
            
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("emsg") == "DUPLICATE":
                response =  requests.post(
                    routes["ftauth"],
                    json = {
                            "UserName": USER,
                            "Password": encode_item(PWD),
                            "App":"",
                            "ClientID":"",
                            "Key":"",
                            "APIKey": API_KEY,
                            "PAN_DOB": pyotp.TOTP(TOTP_KEY).now(),
                            "Sid" : sid,
                            "Override": "Y"
                            },
                        headers= headers
                        )
                if response.status_code == 200:
                    response_data = response.json()
                else:
                    logging.info(response.text)

            redirect_url = response_data.get("RedirectURL", "")

            query_params = parse_qs(urlparse(redirect_url).query)
            if 'code' in query_params:
                code = query_params['code'][0]
                logging.info(code)
                return code
        else:
            logging.info(response.text)
    else:
        logging.info(response.text)

def get_apitoken(code):
    response = requests.post(
        routes["apitoken"],
        json = {
            "api_key": API_KEY,
            "request_code": code, 
            "api_secret": encode_item(f"{API_KEY}{code}{API_SECRET}")
            },
            headers= headers
        )
    
    if response.status_code == 200:
        token = response.json().get("token", "")            
        return token
    else:
        logging.info(response.text)


if __name__ == "__main__":
    code = get_authcode()
    token = get_apitoken(code)
    print(f"CODE :: {code}")
    print(f"SESSION_TOKEN :: {token}")
    api = NorenApiPy()
    ret = api.set_session(
            userid=USER, password=PWD, usertoken=token
    )
    logging.info(f"Is session validated? {ret}")


    