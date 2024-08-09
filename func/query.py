import requests
from collections import defaultdict
from lxml.html import fromstring
from time import sleep
import re
from pathlib import Path
import subprocess
from bs4 import BeautifulSoup
import time
import os

def set_cookies(session, cookies):
    for name, value in cookies.items():
        session.cookies.set(name, value)

def get_atcoder(username):
    try:
        response = requests.get(f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/ac_rank?user={username}");

        if response.status_code == 200:
            data = response.json()
            return data["count"]
        else:
            return -1
    except:
        return -1

def get_codeforces(username):
    try:
        # setup()
        response = requests.get(f"https://codeforces.com/profile/{username}")
        if response.status_code == 200:
            tree = fromstring(response.text)
            ac_count_text = tree.xpath('//*[@id="pageContent"]/div[4]/div/div[3]/div[1]/div[1]/div[1]/text()')[0]
            return int(ac_count_text.split()[0])
        else:
            return -1
    except:
        return -1

def get_hkoi(username):
    url = f"https://judge.hkoi.org/user/{username}"
    cookies_value = os.getenv('cookies')
    cookies = {
        'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d': cookies_value
    }
    session = requests.Session()
    set_cookies(session, cookies)
    response = session.get(url) 
    if response.status_code != 200:
        raise Exception(f"Failed to load page {url}")

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup)
        for h2_element in soup.find_all("h2"):
            print(h2_element.text)
            if "Solved Tasks" in h2_element.text:
                text = h2_element.text
                break
        else:
            text = None
        ac_count = re.search(r"\((\d+)\)", text).group(1)
        return ac_count
    except:
        return -1

def get_platform_ac_count(platform, username):
        ac_count = -1
        if platform == "hkoi":
            ac_count = get_hkoi(username)
        elif platform == "cf":
            ac_count = get_codeforces(username)
        elif platform == "at":
            ac_count = get_atcoder(username)
        return ac_count
    
# print(get_atcoder("kotnid"))
# print(get_codeforces("tkt0506tkt"))
# print(get_hkoi("sms24112"))
# setup()