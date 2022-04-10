import json
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADER = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"}

dd_cookies = [

]

now_use = 0

proxies = {
    'http':'http://127.0.0.1:30001',
    'https':'http://127.0.0.1:30001'
}

proxies_abroad = {
    'http':'http://127.0.0.1:30002',
    'https':'http://127.0.0.1:30002'
}

proxies = None
proxies_abroad = None

def search_by_type(search_type, keyword, page = 1):
    url = "http://api.bilibili.com/x/web-interface/search/type?search_type=%s&keyword=%s&page=%s" % (search_type, keyword, page)
    try:
        r = requests.get(url, headers = HEADER, proxies = proxies)
        r = json.loads(r.text)
    except:
        print("error occured!")
    if r == None or r['code'] != 0:
        return
    return r['data']

def search_user(name):
    r = search_by_type("bili_user", name, 1)
    if r == None:
        return
    first_user = r['result'][0]['mid']
    for i in range(1, r['numPages'] + 1):
        for u in r['result']:
            if u['uname'] == name:
                return u
        r = search_by_type("bili_user", name, i + 1)
        if r == None:
            return
    return first_user

def get_info(mid):
    url = "http://account.bilibili.com/api/member/getCardByMid?mid=" + str(mid)
    try:
        r = requests.get(url, headers = HEADER, proxies = proxies)
        r = json.loads(r.text)
    except Exception as e:
        print(e)
    if r == None or r['code'] != 0:
        return
    return r['card']

def get_medal(mid):
    global dd_cookies
    global now_use
    url = "http://api.live.bilibili.com/xlive/web-ucenter/user/MedalWall?target_id=" + str(mid)
    header = HEADER
    header['cookie'] = dd_cookies[now_use]
    now_use += 1
    if now_use >= 3:
        now_use = 0
    try:
        r = requests.get(url, headers = HEADER, proxies = proxies)
        r = json.loads(r.text)
    except:
        print("error occured")
    if r == None or r['code'] != 0:
        return
    return r['data']

def get_vtb_info():
    r = requests.get("http://api.tokyo.vtbs.moe/v1/short", proxies = proxies_abroad, verify = False)
    return r.text

def download_img(url, name):
    try:
        r = requests.get(url, headers = HEADER, stream = True)
        if r.status_code == 200:
            open(name, 'wb').write(r.content) 
    except :
        print("error occured")
        return False
    else:
        return True    