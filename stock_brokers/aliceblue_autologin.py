# pip install requests cryptography pyotp
import requests
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib
import base64
import pyotp
import os

def auto_alice_v2_login_for_trader(userId, password, totp_encrypt_key):
    class CryptoJsAES:
        @staticmethod
        def __pad(data):
            BLOCK_SIZE = 16
            length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
            return data + (chr(length)*length).encode()
    
        @staticmethod
        def __unpad(data):
            return data[:-(data[-1] if isinstance(data[-1], int) else ord(data[-1]))]
    
        @staticmethod
        def __bytes_to_key(data, salt, output=48):
            assert len(salt) == 8, len(salt)
            data += salt
            key = hashlib.md5(data).digest()
            final_key = key
            while len(final_key) < output:
                key = hashlib.md5(key + data).digest()
                final_key += key
            return final_key[:output]
    
        @staticmethod
        def encrypt(message, passphrase):
            salt = os.urandom(8)
            key_iv = CryptoJsAES.__bytes_to_key(passphrase, salt, 32+16)
            key = key_iv[:32]
            iv = key_iv[32:]
            aes = Cipher(algorithms.AES(key), modes.CBC(iv))
            return base64.b64encode(b"Salted__" + salt + aes.encryptor().update(CryptoJsAES.__pad(message)) + aes.encryptor().finalize())
    
        @staticmethod
        def decrypt(encrypted, passphrase):
            encrypted = base64.b64decode(encrypted)
            assert encrypted[0:8] == b"Salted__"
            salt = encrypted[8:16]
            key_iv = CryptoJsAES.__bytes_to_key(passphrase, salt, 32+16)
            key = key_iv[:32]
            iv = key_iv[32:]
            aes = Cipher(algorithms.AES(key), modes.CBC(iv))
            return CryptoJsAES.__unpad(aes.decryptor.update(encrypted[16:]) + aes.decryptor().finalize())
    print("entered to login for trader {}".format(userId))
    BASE_URL="https://ant.aliceblueonline.com/rest/AliceBlueAPIService"
    twofa = pyotp.TOTP(totp_encrypt_key, digits=4).now()
    totp = pyotp.TOTP(totp_encrypt_key)
    url = BASE_URL+"/customer/getEncryptionKey"
    payload = json.dumps({
        "userId": userId
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload,verify=True)
    
    encKey = response.json()["encKey"]
    
    checksum = CryptoJsAES.encrypt(password.encode(), encKey.encode()).decode('UTF-8')
    
    
    url = BASE_URL+"/customer/webLogin"
    
    payload = json.dumps({
        "userId": userId,
        "userData": checksum
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload,verify=True)
    
    response_data = response.json()
    
    
    url = BASE_URL+"/sso/2fa"
    
    payload = json.dumps({
        "answer1": twofa,
        "userId": userId,
        "sCount": str(response_data['sCount']),
        "sIndex": response_data['sIndex']
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload,verify=True)
    
    
    if response.json()["loPreference"] == "TOTP" and response.json()["totpAvailable"]:
      url = BASE_URL+"/sso/verifyTotp"
    
      payload = json.dumps({
        "tOtp": totp.now(),
        "userId": userId
      })
    
      headers = {
        'Authorization': 'Bearer '+ userId +' '+response.json()['us'],
        'Content-Type': 'application/json'
      }
    
      response = requests.request("POST", url, headers=headers, data=payload,verify=True)
      print(f"{response.json()=}")
      if response.json()["userSessionID"]:
          print("Login Successfully")
    else:
        print("User is not enable TOTP! Please enable TOTP through mobile or web")

with open('creds.json') as f:
    creds = json.load(f)
auto_alice_v2_login_for_trader(creds["user_id"],creds["password_"],creds["totp"])
