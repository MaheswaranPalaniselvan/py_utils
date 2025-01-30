import pyotp
from NorenRestApiPy.NorenApi import NorenApi


cred_dict = {
    "username":"username",
    "pwd" : "pwd",
    "factor2" : "factor2",
    "app_key" : "app_key",
    "imei" : "abc1234"
    }


host = "https://api.shoonya.com/NorenWClientTP/"
websocket = "wss://api.shoonya.com/NorenWSTP/"
# eodhost = "https://api.shoonya.com/chartApi/getdata/"

shoonya_obj = NorenApi(host, websocket)


ret = shoonya_obj.login(
    userid=cred_dict["username"],
    password=cred_dict["pwd"],
    twoFA=str(pyotp.TOTP(cred_dict["factor2"]).now()),
    vendor_code=cred_dict["username"]+'_U',
    api_secret=cred_dict["app_key"],
    imei=cred_dict["imei"],
)

if ret["stat"] == "Ok":
    print(shoonya_obj.get_limits())

    