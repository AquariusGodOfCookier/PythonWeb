from flask import Flask,render_template,redirect,request,jsonify
import pymongo
from pymongo import MongoClient
import json
import requests
import hashlib
import pymysql
import logging
import datetime
import DB
app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    response = request.cookies.get('WTF')
    
    if response is None:
        return render_template('index.html')
    else:
        try:
            responseep =  response.replace('%5B%22','').replace('%20%22','').replace('%22%5D','').replace('%22','').split(',')
            loadtid = responseep[0]
            loadname =responseep[1]
            loadpwd = responseep[2]
            who = responseep[3]
            is_login = checkIsLogin(loadtid,loadpwd,who)
            print('27行',is_login)
            if is_login == 'error':
                return render_template('index.html')
            elif is_login == 'stu':
                return render_template('/student/information.html')
            elif is_login == 'tea':
                return render_template('/teacher/index.html')
            # return render_template('/student/StudentInfor.html')
        except:
            return render_template('index.html')

def checkIsLogin(a,b,who):
    isLogin = DB.conn(a,b,who)
    if isLogin is None:
        return 'error'
    else:
        return who

@app.route('/studentLogin',methods=['POST'])
def studentLogin():
    studentid = request.values.get('studentid')
    studentpassword = request.values.get('studentpassword')
    query = DB.conn(studentid,studentpassword,'stu')
    if query is None:
        return 'error'
    else:
        studentid = query[0]
        studentname = query[1]
        studentPwd  = query[2]
        a = [studentid,studentname,studentPwd]
        return json.dumps(a)


@app.route('/student')
def student():
    response = request.cookies.get('WTF')
    if response is None:
        return render_template('index.html')
    else:
        try:
            responseep =  response.replace('%5B%22','').replace('%20%22','').replace('%22%5D','').replace('%22','').split(',')
            loadtid = responseep[0]
            loadname =responseep[1]
            loadpwd = responseep[2]
            who = responseep[3]
            is_login = checkIsLogin(loadtid,loadpwd,who)
            if is_login == 'stu':
                return render_template('/student/information.html')
            else:
                 return render_template('index.html')
        except:
            return render_template('index.html')

@app.route('/teacherLogin',methods=['POST'])
def teacherLogin():
    teacherid = request.values.get('teacherid')
    teacherpassword = request.values.get('teacherpassword')
    query = DB.conn(teacherid,teacherpassword,'tea')
    if query == 'None':
        return 'error'
    else:
        teacherid = query[0]
        teachername = query[1]
        teachernpwd  = query[3]
        a = [teacherid,teachername,teachernpwd]
        return json.dumps(a)

@app.route('/teacher')
def teacher():
    response = request.cookies.get('WTF')
    if response is None:
        return response
    else:
        try:
            responseep =  response.replace('%5B%22','').replace('%20%22','').replace('%22%5D','').replace('%22','').split(',')
            loadtid = responseep[0]
            loadname =responseep[1]
            who = responseep[2]
            if who == 'tea':
                return render_template('/teacher/index.html')
            else:
                 return render_template('index.html')
        except:
            return 'error'



#这块是学生前端跳转部分
@app.route('/MyScore')
def MyScore():
    response = request.cookies.get('WTF')
    if response is None:
        return render_template('index.html')
    else:
        try:
            responseep =  response.replace('%5B%22','').replace('%20%22','').replace('%22%5D','').replace('%22','').split(',')
            loadtid = responseep[0]
            loadname =responseep[1]
            loadpwd = responseep[2]
            who = responseep[3]
            is_login = checkIsLogin(loadtid,loadpwd,who)
            if is_login == 'stu':
                return render_template('/student/MyScore.html')
            else:
                 return render_template('index.html')
        except:
            return render_template('index.html')

@app.route('/PasChange')
def PasChange():
    response = request.cookies.get('WTF')
    if response is None:
        return render_template('index.html')
    else:
        try:
            responseep =  response.replace('%5B%22','').replace('%20%22','').replace('%22%5D','').replace('%22','').split(',')
            loadtid = responseep[0]
            loadname =responseep[1]
            loadpwd = responseep[2]
            who = responseep[3]
            is_login = checkIsLogin(loadtid,loadpwd,who)
            print('150',loadtid,loadname,loadpwd,is_login)
            if is_login == 'stu':
                return render_template('/student/PasChange.html')
            else:
                 return render_template('index.html')
        except:
            return render_template('index.html')

@app.route('/table')
def table():
    response = request.cookies.get('WTF')
    if response is None:
        return render_template('index.html')
    else:
        try:
            responseep =  response.replace('%5B%22','').replace('%20%22','').replace('%22%5D','').replace('%22','').split(',')
            loadtid = responseep[0]
            loadname =responseep[1]
            loadpwd = responseep[2]
            who = responseep[3]
            is_login = checkIsLogin(loadtid,loadpwd,who)
            if is_login == 'stu':
                return render_template('/student/table.html')
            else:
                 return render_template('index.html')
        except:
            return render_template('index.html')

@app.route('/StudentInfor')
def StudentInfor():
    response = request.cookies.get('WTF')
    if response is None:
        return render_template('index.html')
    else:
        try:
            responseep =  response.replace('%5B%22','').replace('%20%22','').replace('%22%5D','').replace('%22','').split(',')
            loadtid = responseep[0]
            loadname =responseep[1]
            loadpwd = responseep[2]
            who = responseep[3]
            is_login = checkIsLogin(loadtid,loadpwd,who)
            if is_login == 'stu':
                return render_template('/student/StudentInfor.html')
            else:
                 return render_template('index.html')
        except:
            return render_template('index.html')

#学生修改密码
@app.route('/ChangePass',methods=['POST'])
def ChangePass():
    studentId = request.values.get('studentId')
    OldPassword = request.values.get('OldPassword')
    NewPassword = request.values.get('NewPassword')
    try:
        isStudent = DB.isLoad(OldPassword,studentId)
        #如果原密码正确，那就修改密码
        if isStudent == 'OK':
            changepas = DB.changepas(NewPassword,studentId)
            if changepas == 'OK':
                return 'OK'
            elif changepas == 'ERROR':
                return 'ERROR'
        elif isStudent =='none':
            return 'none'
        else:
            return 'ERROR'
    except:
        return 'ERROR'

#学生查询学期课表
@app.route('/Handle',methods=['POST'])
def Handle():
    studentId = request.values.get('studentId')
    yearsValue = request.values.get('yearsValue')
    saValue = request.values.get('saValue')
    a = [studentId,yearsValue,saValue]
    if saValue=='1':
        saValue='春'
    elif saValue == '2':
        saValue='秋'
    try:
        list = []
        tables = DB.Handle(studentId,yearsValue,saValue)
        for i in tables:
            list+=[i]
        return json.dumps(list)
    except:
        return 'error'

#个人成绩查询
@app.route('/QMyScore',methods=['POST'])
def QMyScore():
    studentId = request.values.get('studentId')
    yearsValue = request.values.get('yearsValue')
    saValue = request.values.get('saValue')
    a = [studentId,yearsValue,saValue]
    if saValue=='1':
        saValue='春'
    elif saValue == '2':
        saValue='秋'
    try:
        list = []
        tables = DB.QMyScore(studentId,yearsValue,saValue)
        for i in tables:
            list+=[i]
        return json.dumps(list)
    except:
        return 'error'

#个人信息查询
@app.route('/QstudentQuery',methods=['POST'])
def QstudentQuery():
    studentId = request.values.get('studentId')
    try:
        list = []
        tables = DB.QstudentQuery(studentId)
        for i in tables:
            list+=[i]
        return json.dumps(list)
    except:
        return 'error'

#这块是老师前端跳转部分
@app.route('/teaPasChange')
def teaPasChange():
    return render_template('/teacher/teacherCP.html')
@app.route('/teatable')
def teatable():
    return render_template('/teacher/teatable.html')
#教师修改密码
@app.route('/TeacherChangePass',methods=['POST'])
def TeacherChangePass():
    teacherid = request.values.get('teacherid')
    OldPassword = request.values.get('OldPassword')
    NewPassword = request.values.get('NewPassword')
    # a = [teacherid,OldPassword,NewPassword]
    # return json.dumps(a)
    try:
        isteacher = DB.isLoad(OldPassword,teacherid)
        # return isteacher
        #如果原密码正确，那就修改密码
        if isteacher == 'OK':
            changepas = DB.changepas(NewPassword,teacherid)
            if changepas == 'OK':
                return 'OK'
            elif changepas == 'ERROR':
                return 'ERROR'
        elif isteacher =='none':
            return 'none'
        else:
            return 'ERROR'
    except:
        return 'ERROR'

#教师端打分
@app.route('/Qteacher',methods=['POST'])
def Qteacher():
    teacherid = request.values.get('teacherid')
    Qteachers = DB.Qteacher(teacherid)
    a = {}
    for i in Qteachers:
        a.setdefault(i,[]).append(Qteachers[i])
    return json.dumps(a)

#教师端修改学生成绩
@app.route('/Cgrade',methods=['POST'])
def Cgrade():
    cname = request.values.get('cname')
    sid = request.values.get('sid')
    score = request.values.get('numinputs')
    cid = DB.getcid(cname)
    try:
        a = DB.Cgrade(sid,cid,score)
        return a
    except:
        return 'error'

if __name__ == '__main__':
    app.run(debug = True,port="3390")
    
  