import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'raise_on_warnings': True,
}

DB_NAME = 'zimuzu'

TABLES = {}

TABLES['info'] = (
    "CREATE TABLE `info` ("
    "  `id` int(10) UNSIGNED NOT NULL ,"
    "  `state` tinyint(2) UNSIGNED,"
    "  `cnname` varchar(200),"
    "  PRIMARY KEY (`id`)"
    ") ")

TABLES['resource_item'] = (
    "CREATE TABLE `resource_item` ("
    "  `id` int(10) UNSIGNED NOT NULL,"
    "  `resourceid` int(10) UNSIGNED NOT NULL,"
    "  `name` varchar(200),"
    "  `format` varchar(200),"
    "  `season` tinyint(2) UNSIGNED NOT NULL DEFAULT 0,"
    "  `episode` tinyint(2) UNSIGNED NOT NULL DEFAULT 0,"
    "  `size` varchar(20) NOT NULL DEFAULT 0,"
    "  `ed2k` text,"
    "  `magnet` text,"
    "  PRIMARY KEY (`id`)"
    ") ")


def connect(config):
    global cnx
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            exit(1)
    else:
        return cnx

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def init():
    cnx  = connect(config)
    cursor = cnx.cursor()
    try:
        cnx.database = DB_NAME
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            cnx.database = DB_NAME
        else:
            print(err)
            cursor.close()
            cnx.close()
            exit(1)

    for name, ddl in TABLES.items():
        try:
            print("Creating table {}: ".format(name), end='')
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    return "Init Done!"

if __name__=='__main__':
    print(init())
