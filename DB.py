import pymysql
import logging
import datetime
import json
def conn(id,pwd,type):
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
  sql = "SELECT * FROM login where usertype='%s' and id = '%s' and password='%s'"%(type,id,pwd)
  try:
   # 执行SQL语句
    cursor.execute(sql)
   # 获取所有记录列表
    results = cursor.fetchone()
    return results
  except:
    return "ERROR"

 # 关闭数据库连接
  cursor.close()

def changepas(NewPd,Id):
  con=pymysql.connect(
    host='127.0.0.1',
    port=3308,
    user='',
    password='',
    db='student',
    charset='utf8'
    )
  cursor = con.cursor()
  # SQL 修改语句
  sql = "UPDATE login set password = '%s' where id = '%s'"%(NewPd,Id)
  try:
   # 执行SQL语句
    cursor.execute(sql)
    con.commit()
    con.close()
    cursor.close()
   # 获取所有记录列表
    return "OK"

  except:
    return "ERROR"
  

def isLoad(password,id):
  con=pymysql.connect(
    host='127.0.0.1',
    port=3308,
    user='',
    password='',
    db='student',
    charset='utf8'
    )
  cursor = con.cursor()
  sql = "SELECT password FROM login where id = '%s'"%(id)
  try:
    cursor.execute(sql)
    results = cursor.fetchone()
    for i in results:
      if i == password:
        return 'OK'
      else:
        return 'none'
  except:
    return 'Error'
  
def Handle(id,years,season):
  con=pymysql.connect(
    host='127.0.0.1',
    port=3308,
    user='',
    password='',
    db='student',
    charset='utf8'
    )
  cursor = con.cursor()
  # SQL 修改语句
  sql = "select course.cid , course.cname ,course.credit,teacher.tname from choosecourse,course,teacher where  course.season = '%s' and course.years = '%s' and choosecourse.cid=course.cid and choosecourse.tid=teacher.tid and choosecourse.sid='%s'"%(season,years,id)
  try:
   # 执行SQL语句
    cursor.execute(sql)
   # 获取所有记录列表
    results = cursor.fetchall()
    return results

  except:
    return "ERROR"

def QMyScore(id,years,season):
  con=pymysql.connect(
    host='127.0.0.1',
    port=3308,
    user='',
    password='',
    db='student',
    charset='utf8'
    )
  cursor = con.cursor()
  # SQL 修改语句
  sql = "select course.cname,grade.score,grade.credit,grade.examtype from grade,course where  grade.sid='%s' and grade.cid = course.cid and grade.season = '%s' and grade.time='%s'"%(id,season,years)
  try:
   # 执行SQL语句
    cursor.execute(sql)
   # 获取所有记录列表
    results = cursor.fetchall()
    return results

  except:
    return "ERROR"
  

def QstudentQuery(id):
  con=pymysql.connect(
    host='127.0.0.1',
    port=3308,
    user='',
    password='',
    db='student',
    charset='utf8'
    )
  cursor = con.cursor()
  # SQL 修改语句
  sql = "select * from studentinfor where studentinfor.id = '%s'"%(id)
  try:
   # 执行SQL语句
    cursor.execute(sql)
   # 获取所有记录列表
    results = cursor.fetchall()
    return results

  except:
    return "ERROR"

def Qteacher(id):
  con=pymysql.connect(
    host='127.0.0.1',
    port=3308,
    user='',
    password='',
    db='student',
    charset='utf8'
    )
  cursor = con.cursor()
  # SQL 修改语句
  sql = "select choosecourse.sid ,choosecourse.cid ,course.cname from choosecourse , course where choosecourse.tid = '%s' and course.cid = choosecourse.cid"%(id)
  cursor.execute(sql)
  results = cursor.fetchall()
  mystudent = {}
  mysubject = []
  ss = []
  for i in results:
    student = i[0]
    subject = i[2]
    cid = i[1]
    grade = str(Qgrade(student,cid))
    studentname = Qname(student)
    ss = [student,studentname,grade]
    mystudent.setdefault(subject,[]).append(ss)
  return mystudent


def Qname(id):
  con=pymysql.connect(
    host='127.0.0.1',
    port=3308,
    user='',
    password='',
    db='student',
    charset='utf8'
    )
  cursor = con.cursor()
  # SQL 修改语句
  try:
    sql = "select name from login where login.id = '%s'"%(id)
    cursor.execute(sql)
    results = cursor.fetchone()
    for i in results:
      return i
  except:
    return 'none'

def Qgrade(studentid,cid):
  con=pymysql.connect(
    host='127.0.0.1',
    port=3308,
    user='',
    password='',
    db='student',
    charset='utf8'
    )
  cursor = con.cursor()
  # SQL 修改语句
  try:
    sql = "select grade.score from grade,login where login.id = '%s' and grade.sid = '%s' and grade.cid = '%s'"%(studentid,studentid,cid)
    cursor.execute(sql)
    results = cursor.fetchone()
    for i in results:
      return i
  except:
    return 'none'

def getcid(cname):
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
  sql = "SELECT cid FROM course where cname = '%s'"%(cname)
  try:
   # 执行SQL语句
    cursor.execute(sql)
   # 获取所有记录列表
    results = cursor.fetchone()
    for i in results:
      return i

  except:
    return "ERROR"

def Cgrade(sid,cid,score):
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
  sql = "SELECT credit,season,years FROM course where cid = '%s'"%(cid)
   # 执行SQL语句
  cursor.execute(sql)
   # 获取所有记录列表
  results = cursor.fetchall()
  for i in results:
    credit = i[0]
    season = i[1]
    time = i[2]
    a = [credit,season,time]
    # UpdateGrade(sid,cid,score)
  ##检查他是走添加还是修改
  asql = "select score from grade where sid = '%s' and cid = '%s'"%(sid,cid)
  cursor.execute(asql)
  aresults = cursor.fetchone()
  ##如果没有成绩，那就让他添加程序
  if aresults is None:
    a = AlertGrade(sid,cid,score,credit,season,time)
    return a
  else:
    b = UpdateGrade(sid,cid,score)
    return b


def AlertGrade(sid,cid,score,credit,season,time):
  con=pymysql.connect(
    host='127.0.0.1',
    port=3308,
    user='',
    password='',
    db='student',
    charset='utf8'
    )
  cursor = con.cursor()
  # SQL 修改语句
  sql = "insert into grade (sid,cid,score,credit,season,time) values('%s','%s','%s','%s','%s','%s')"%(sid,cid,score,credit,season,time)
  # 执行SQL语句
  try:
    cursor.execute(sql)
    con.commit()
    con.close()
    cursor.close()
   # 获取所有记录列表
    return "AlertGradeSuccess"
  except:
    return "AlertGradeFail"

def UpdateGrade(sid,cid,score):
  con=pymysql.connect(
    host='127.0.0.1',
    port=3308,
    user='',
    password='',
    db='student',
    charset='utf8'
    )
  cursor = con.cursor()
  sql = "update grade set score='%s' where sid ='%s' and cid ='%s'"%(score,sid,cid)
  cursor.execute(sql)
  con.commit()
  con.close()
  cursor.close()
  return 'ok'

# print(conn('1604010201','1','stu'))
# print(isLoad('100001','100001'))
# changepas('NewPassword','100001')
# print(Qgrade('1604010201','040115HI02W1'))
# print(Qname('1604010201'))
# print(Qteacher('100001'))
# print(getcid('程序设计基础'))
# print(Cgrade('1604010203','040115HI02W1','78'))
#print(AlertGrade('1604010202','040115HI02W1','78','4.5','春','2019'))
# print(UpdateGrade('1604010202','040115HI02W1','88'))