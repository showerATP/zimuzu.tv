import mysql.connector
from mysql.connector import errorcode

def save(cnx, id, **kw):

    cursor = cnx.cursor()
    if not find(cnx, id):
        info = ("INSERT info (id) VALUES (%s)")
        try:
            cursor.execute(info, (id, ))
        except mysql.connector.Error as err:
            raise

    for key in kw:
        info = ("UPDATE info SET " + key + " = %s WHERE id = %s")
        try:
            cursor.execute(info, (kw[key], id))
        except mysql.connector.Error as err:
            raise

    cnx.commit()
    return

def find(cnx, id):
    cursor = cnx.cursor(dictionary=True)
    query = ("SELECT * FROM info WHERE id = %s")

    try:
        cursor.execute(query, (id, ))
    except mysql.connector.Error as err:
        raise

    info = cursor.fetchone()
    return info

if __name__=='__main__':
    info = {'id': 5, 'state': 0, 'cnname': "中文"}
    #save(**info)
    print(find(27017))
