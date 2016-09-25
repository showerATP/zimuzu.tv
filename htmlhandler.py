

from bs4 import BeautifulSoup
import threading
from multiprocessing import Pool
import os
import time
import mysql.connector


def saveHtml(path, data):
    with open(path, 'w') as f:
        return f.write(data)

def handle(f):
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

def zmz(id):
    start = time.time()
    #conn = mysql.connector.connect(user='root', password='root', database='zimuzu')
    #cursor = conn.cursor()
    for i in range(id, 35000):
        path = "html/"+str(i)+".html"
        if not os.path.exists(path):
            print(i,"LOST")
            #f = getHtml("html/"+str(i)+".html")
            f = getHtml(base+str(i))
            state = handle(f)
            saveHtml(path, f)

            #cursor.execute('insert into resource (id, state) values (%s, %s)', [i, state])
    #conn.commit()
    #cursor.close()
    #conn.close()
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (id, (end - start)))
    return

zmz(10000)

if __name__=='__main_':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(12000,35000,50):
        p.apply_async(zmz, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    start = time.time()
    p.join()
    end = time.time()
    print('All subprocesses done, %0.2f seconds.' % (end - start))
