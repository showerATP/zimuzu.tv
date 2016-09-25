

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from sys import stdout
import re
import requests
import threading
from multiprocessing import Pool
import os
import time
from getPage import getInfoPage
from getPage import getResPage
from db import connect
from dbRes import save
from dbRes import find
import dbInfo
import mysql.connector
from mysql.connector import errorcode

def getRes(f):
    bsObj = BeautifulSoup(f, 'html5lib')
    lists = bsObj.findAll(class_ = "media-list")
    items = []
    for list in lists:
        lis = list.findAll("li")
        for li in lis:
            item = {}

            item["format"] = li["format"]

            season = li["season"]
            if season:
                item["season"] = season
            else:
                item["season"] = 0

            episode = li["episode"]
            if episode:
                item["episode"] = episode
            else:
                item["episode"] = 0

            a = li.find(class_ = "fl").a
            if a:
                item["name"] = a["title"]
                item["itemid"] = a["itemid"]

            font = li.find(class_ = "fl").font
            if font:
                item["size"] = font.get_text()

            ed2k = li.find(class_ = "fr").find(type="ed2k")
            if ed2k:
                item["ed2k"] = ed2k["href"]

            magnet = li.find(class_ = "fr").find(type="magnet")
            if magnet:
                item["magnet"] = magnet["href"]
            items.append(item)
    return items

def get(id):
    start = time.time()

    cnx = connect()
    no = 0

    for i in range(id, id+50):
        try:
            info = dbInfo.find(cnx, i)
        except mysql.connector.Error as err:
            print(i, "FIND ERR", err)
            continue
        if info["state"] == 1:
            try:
                f = getResPage(i)
            except requests.exceptions.RequestException as err:
                print(i, err)
                continue
            items = getRes(f)
            for item in items:
                item["resourceid"] = i
                try:
                    save(cnx,**item)
                except mysql.connector.Error as err:
                    print(i, "SAVE ERR", err)
                    continue
            print(i, "Done")

    cnx.close()

    end = time.time()
    print('Task %s runs %0.2f seconds.  %d' % (id, (end - start), no))
    return

if __name__=='_main__':
    get(11019)

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(8)
    for i in range(20000,35000,50):
        p.apply_async(get, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    start = time.time()
    p.join()
    end = time.time()
    print('All subprocesses done, %0.2f seconds.' % (end - start))
