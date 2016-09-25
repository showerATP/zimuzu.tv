


import mysql.connector

conn = mysql.connector.connect(user='root', password='root', database='zimuzu')
cursor = conn.cursor()

#cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
#cursor.execute('insert into user (id, name) values (%s, %s)', ['1', 'Michael'])

cursor.rowcount

conn.commit()
cursor.close()

cursor = conn.cursor()
for i in range(10000, 35000):
    cursor.execute('select * from resource where id = %s', (i,))
    values = cursor.fetchall()
    if not values:
        print(i)

cursor.close()

conn.close()
