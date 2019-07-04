import pymysql
import logging
import datetime
def conn(e):
  con=pymysql.connect(
    host='127.0.0.1',
    port=3308,
    user='',
    password='',
    db='student',
    charset='utf8'
    )
  cursor = con.cursor()

# SQL 查询语句
  sql = "SELECT * FROM "+e
  try:
   # 执行SQL语句
    cursor.execute(sql)
   # 获取所有记录列表
    results = cursor.fetchall()
    for it in results:
	    for i in range(len(it)):
		    print (it[i],' ')
	    print ('\n')
  except:
    print ("Error: unable to fecth data")

# 关闭数据库连接
  cursor.close()

def insert_login(a,b):
   con=pymysql.connect(
    host='192.168.43.220',
    port=3308,
    user='root',
    password='tiger',
    db='musicplay',
    charset='utf8'
    )
   cursor = con.cursor()
   sql = "insert into login values('%s', '%s')" %(a,b)
   cursor.execute(sql)
   con.commit()
   cursor.close()
   con.close()
def check_login(a,b):
  con=pymysql.connect(
    host='192.168.43.220',
    port=3308,
    user='root',
    password='tiger',
    db='musicplay',
    charset='utf8'
    )
  cursor = con.cursor()
  sql = "SELECT * FROM login where username=%s"
  try:
    cursor.execute(sql,(a))
    results = cursor.fetchall()
    if len(results)==0:
      return 3
    password=results[0][1]
    if password==b:
      return 1
    else:
      return 2
  finally:
    cursor.close()
    con.close()
def insert_music_info(a,b):
   con=pymysql.connect(
    host='192.168.43.220',
    port=3308,
    user='root',
    password='tiger',
    db='musicplay',
    charset='utf8'
    )
   cursor = con.cursor()
   print(a,b)
   c=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   print(c)
   sql = "insert into music_info values('%s', '%s','%s')" %(a,b,c)
   cursor.execute(sql)
   con.commit()
   cursor.close()
   con.close()

conn('login')