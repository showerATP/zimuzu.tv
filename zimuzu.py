

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

from login import getCookie

def getHtml(url):
    global cookies
    r = requests.get(url, cookies = cookies)
    return r.text

def saveHtml(path, data):
    with open(path, 'w') as f:
        return f.write(data)

def zmz(id):
    global base
    #print('Run task %s (%s)...' % (id, os.getpid()))
    start = time.time()
    for i in range(id,id+50):
        saveHtml("html/"+str(i)+".html", getHtml(base+str(i)))
        #print(str(i),"Done")
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (id, (end - start)))
    return



base = 'http://www.zimuzu.tv/fresource/list/'
cookies = getCookie()

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(16)
    for i in range(10000,35000,50):
        p.apply_async(zmz, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    start = time.time()
    p.join()
    end = time.time()
    print('All subprocesses done, %0.2f seconds.' % (end - start))
