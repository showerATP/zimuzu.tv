import mysql.connector
from mysql.connector import errorcode

def save(cnx, itemid, **kw):

    cursor = cnx.cursor()
    if not find(cnx, itemid):
        info = ("INSERT resource_item (itemid) VALUES (%s)")
        try:
            cursor.execute(info, (itemid, ))
        except mysql.connector.Error as err:
            raise

    for key in kw:
        info = ("UPDATE resource_item SET " + key + " = %s WHERE itemid = %s")
        try:
            cursor.execute(info, (kw[key], itemid))
        except mysql.connector.Error as err:
            raise

    cnx.commit()
    return

def find(cnx, itemid):
    cursor = cnx.cursor(dictionary=True)
    query = ("SELECT * FROM resource_item WHERE itemid = %s")

    try:
        cursor.execute(query, (itemid, ))
    except mysql.connector.Error as err:
        raise

    info = cursor.fetchone()
    return info

if __name__=='__main__':
    info = {'id': 5, 'state': 0, 'cnname': "中文"}
    #save(**info)
    print(find(27017))
