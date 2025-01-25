import requests
import pyotp
from kiteconnect import KiteConnect

def autologin(user_id, password, totp_key, api_key, api_secret):
    try:
        reqSession = requests.Session()
        loginurl = "https://kite.zerodha.com/api/login"
        twofaUrl = "https://kite.zerodha.com/api/twofa"
        twofa = f"{pyotp.TOTP(totp_key).now()}"
        request_id = reqSession.post(
            loginurl,
            data={
                "user_id": user_id,
                "password": password,
            },
        ).json()["data"]["request_id"]
        reqSession.post(
            twofaUrl,
            data={"user_id": user_id, "request_id": request_id, "twofa_value": twofa},
        )
        API_Session = reqSession.get("https://kite.trade/connect/login?api_key=" + api_key)
        API_Session = API_Session.url.split("request_token=")
        request_token = API_Session[1].split("&")[0]
        data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = data["access_token"]
        return request_token, access_token, kite
    except Exception as e:
        error_message = str("Desktop Connect Program: Error message: "+str(e))

        print("Error is :",error_message)

kite = KiteConnect(api_key)
autologin(user_id, password, totp_key, api_key, api_secret)
kite.profile()
