#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from login import getCookie
import requests

def getPage(url):
    global cookies

    r = requests.get(url, cookies = cookies)

    return r.text

def getInfoPage(id):
    global infoBase
    return getPage(infoBase + str(id))

def getResPage(id):
    global listBase
    try:
        f = getPage(listBase + str(id))
    except requests.exceptions.RequestException as err:
        if err.args[0].reason.errno == 111:
            getInfoPage(id)
        f = getPage(listBase + str(id))
    return f

cookies = getCookie()
base = "http://www.zimuzu.tv/"
infoBase = base + "gresource/"
listBase = infoBase + "list/"

if __name__=='__main__':
    print(getPage("http://www.baaaaaaidu.com"))
    print("Hello")
