

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
from dbInfo import save
from dbInfo import find

def getState(f):
    bsObj = BeautifulSoup(f, 'html5lib')
    title = bsObj.title.get_text()
    tips = bsObj.find(id = 'resource_view_tips')
    if title == "系统信息提示页":
        state = -1
    elif tips:
        state = 0
    else:
        state = 1
    return state

def getName(f):
    bsObj = BeautifulSoup(f, 'html5lib')
    cnname = bsObj.find(class_ = "box score-box").find("h2").get_text()[:-3]
    return cnname

def get(id):
    #print('Run task %s (%s)...' % (id, os.getpid()))
    start = time.time()

    cnx = connect()

    for i in range(id,id+50):
        info = find(cnx, i)
        if not info:
            print(i)
            state = getState(getResPage(i))
            save(cnx, i,state = state)
            info = find(cnx, i)
        if info['state'] == -1 :
            state = getState(getInfoPage(i))
            save(cnx, i, state = state)

    cnx.close()

    end = time.time()
    print('Task %s runs %0.2f seconds.' % (id, (end - start)))
    return


if __name__=='__main_':
    #print(getName(getInfo(10004)))
    get(28400)

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(30000,35000,50):
        p.apply_async(get, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    start = time.time()
    p.join()
    end = time.time()
    print('All subprocesses done, %0.2f seconds.' % (end - start))
