#!/usr/bin/env python
# coding: utf-8
import requests,re
import json
import sys
from bs4 import BeautifulSoup as bs
state_index = (sys.argv[1])
print (state_index)
filename = sys.argv[2]+".jsonl"
open(filename,"w").write("")
lastPageFromCli = int(sys.argv[3]) or 0
def get_data(ngoid,token):
    cookie = f'ci_session=qra1cna4ijclvtem2hlr7k7v7ej98fe6; csrf_cookie_name={token}'
    print (cookie)
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'Accept': '*/*',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://ngodarpan.gov.in',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/116/35/1',
        'Accept-Language': 'en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,da;q=0.6',
        'Cookie': f'ci_session=qra1cna4ijclvtem2hlr7k7v7ej98fe6; csrf_cookie_name={token}',
        
    }
    data = {
      'id': ngoid,
      'csrf_test_name': token,
    }
    response = requests.post('https://ngodarpan.gov.in/index.php/ajaxcontroller/show_ngo_info', headers=headers,data=data)
    return response
def get_cookie():
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/8046/19/1',
        'Accept-Language': 'en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,da;q=0.6',
        
    }

    response = requests.get('https://ngodarpan.gov.in/index.php/ajaxcontroller/get_csrf', headers=headers)
    return response

def store_data(ngoid,state):
    c = get_cookie()
    active_token = c.json().get('csrf_token')
    data=get_data(ngoid,active_token).json()
    open(f"{filename}","a").write(json.dumps(data)+"\n")

def gotopage(homepage,pagenum):
    root = "https://ngodarpan.gov.in/index.php/home/statewise_ngo/"
    numsections = homepage.replace(root,"").split("/")
    numsections[-1] = str(pagenum)
    newHomePage = root+"/".join(numsections)
    return newHomePage

def process_state(state):
    last_page = None
    statehtml = requests.get(state)
    try:
        for link in bs(statehtml.content).select("a"):
            if link.text == "Last":
                last_page=link.attrs["data-ci-pagination-page"]
    except:
        pass
    if not last_page:
        last_page = lastPageFromCli
    for i in range(1,int(last_page)+1):
        pagetovisit = gotopage(state,i)
        pagehtml = requests.get(pagetovisit,timeout=10).content
        bspagehtml = bs(pagehtml)
        tbl = bspagehtml.select(".ibox-content tbody tr")
        for tr in tbl:
            tds = tr.select("a")[0].attrs["onclick"]
            number = re.sub(r"\D", "", tds)
            print (int(number))
            try:
                store_data(int(number),state_index)
            except Exception as e:
                print (e)
                pass

process_state(state_index)

