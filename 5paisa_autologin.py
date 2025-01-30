from py5paisa import FivePaisaClient
import pyotp

credentials = {
        "APP_NAME": 'APP_NAME',
        "APP_SOURCE": 'APP_SOURCE',
        "USER_ID": 'USER_ID',
        "PASSWORD": 'PASSWORD',
        "USER_KEY": 'USER_KEY',
        "ENCRYPTION_KEY": 'ENCRYPTION_KEY',
        "TOTP_KEY": 'TOTP_KEY',
        "CLIENT_CODE": 'CLIENT_CODE',
        "MPIN": 'MPIN'
    }


client = FivePaisaClient(cred={
    "APP_NAME":credentials['APP_NAME'],
    "APP_SOURCE":credentials['APP_SOURCE'],
    "USER_ID":credentials['USER_ID'],
    "PASSWORD":credentials['PASSWORD'],
    "USER_KEY":credentials['USER_KEY'],
    "ENCRYPTION_KEY":credentials['ENCRYPTION_KEY']
    })
client.get_totp_session(credentials['CLIENT_CODE'], pyotp.TOTP(credentials['TOTP_KEY']).now(), credentials['MPIN'])
client.set_access_token(client.get_access_token(), credentials['CLIENT_CODE'])
print(client.positions())