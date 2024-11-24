import os
import sys

try:
    import requests
except (ModuleNotFoundError, ImportError):
    os.system(f"{sys.executable} -m pip install -U requests")
finally:
    import requests
    
chat_id = "XXX" # From Scan ID
bot_id = "YYY:ZZZZZZ" # From BotFather
def send_msg(msg: str):
    url = f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text="
    _ = requests.get(url+msg)
    
if __name__ == "__main__":
    send_msg("test now!!")
