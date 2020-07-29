import tkinter as tk
import pymysql


mydb = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="Vitol0928!?^^",
        database="pydb"
)
mc = mydb.cursor()
sql="SELECT * FROM 책목록 WHERE 도서명=%s"
val="머신러닝"
mc.execute(sql,val)

mr=mc.fetchall()
for x in mr:
    print(x)

