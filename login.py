#!/usr/bin/python3
# coding=utf-8
import requests
import hashlib
import json
import sys

f = open(sys.path[0]+'/credentials.json', 'r')
credentials = json.load(f.read())
login = credentials['login']
appkey = credentials['appkey']
secret = credentials['secret']
accountkey = credentials['accountkey']
f.close()

def apisign(url, data):
    loadstr = ''
    for i in data:
        if type(data[i]) == type('str'):
            loadstr += ','
            loadstr += data[i]
    loadstr = loadstr[1:]
    loadstr = secret+url+loadstr
    return {'apisign': hashlib.md5(loadstr.encode('utf-8')).hexdigest()}


def getuserkey():
    load = {
        'login': login,
        'accountkey': accountkey
    }
    url = "https://a2.wykop.pl/Login/Index/appkey/{0}/".format(appkey)
    
    r = requests.post(url, data=load, headers=apisign(url, load))
    try:
        result = json.loads(r.text)
    except:
        return 'json error'
    if 'error' in result:
        return 'login error'
    userkey = result['data']['userkey']

    f = open('/tmp/wykoplogin', 'w')
    f.write(userkey)
    f.close()

    return userkey

def quest(url,method='get',data={},filename=''):

    userkey=''
    try:
        f = open('/tmp/wykoplogin', 'r')
        userkey = f.read()
        f.close()
    except:
        userkey = getuserkey()

    for i in range(2):
        files = {
            'embed': (filename, open(filename, 'rb'), 'image/png')
        } if filename else {}
        url+='appkey/{0}/userkey/{1}/'.format(appkey,userkey)

        if(method=='post'):
            r = requests.post(url,  headers=apisign(url, data), data=data,  files=files)
        else:
            r = requests.get(url,  headers=apisign(url, data))
       
        result = json.loads(r.text)
        if i == 0 and 'error' in result and result['error']['code'] in [5, 11, 12]:
                userkey = getuserkey()
        else:
            return result

    return result

def setcontent(message, filename=False, link=False):
    url = "https://a2.wykop.pl/Entries/Add/"
    data = {
        'body': message
    } 
    if link:
        data['embed'] = link
    files = {
        'embed': (filename, open(filename, 'rb'), 'image/png')
    } if filename else {}
    return quest(url,'post',data,filename)



def getranklist(page):
    url = "https://a2.wykop.pl/Profiles/Rank/page/{0}/data/full/".format(page)
    return quest(url)

def getuser(page):
    url = "https://a2.wykop.pl/Profiles/Index/{0}/data/full/".format(page)
    return quest(url)

def getmywykop():
    url = "https://a2.wykop.pl/Mywykop/Index/page/0/type/entries/"
    return quest(url)
