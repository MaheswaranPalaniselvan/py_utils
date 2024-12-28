import requests
import traceback



def get_ltp_from_nse(index='NIFTY 50'):
    url_oc: str = "https://www.nseindia.com/option-chain"
    headers: dict[str, str] = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.nseindia.com/',
        'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }
    session: requests.Session = requests.Session()
    request: requests.Response = session.get(url_oc, headers=headers)
    cookies = dict(request.cookies)
    
    url = 'https://www.nseindia.com/api/equity-stockIndices'
    params = {
        'index': index,
    }
    try:
        response = session.get(url, params=params, headers=headers, timeout=50, cookies=cookies)
        return float(response.json()['metadata']['last'])
    except:
        print(traceback.format_exc())



def get_ltp_from_bse(index='SENSEX'):
    headers: dict[str, str]  = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.bseindia.com/',
        'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }
    index_to_code = {'SENSEX': '16'}
    params = {
        'code': index_to_code[index],
    }
    response = requests.get('https://api.bseindia.com/BseIndiaAPI/api/GetLinknew/w', params=params, headers=headers)
    try:
        return float(response.json()['CurrValue'].replace(',', ''))
    except:
        print(traceback.format_exc())


if __name__ == "__main__":
    print(get_ltp_from_nse('NIFTY 50'))
    print(get_ltp_from_nse('NIFTY BANK'))
    print(get_ltp_from_bse('SENSEX'))