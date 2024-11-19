from flask import render_template,request,redirect, flash,session
from flask import Blueprint

from ATMflask import db
from ATMflask.sql import User
import pymysql

myInfo = Blueprint('myInfo',__name__)

@myInfo.route('/MyInformation',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def myinformation():
    user_id = session.get('id')

    user = User.query.get(user_id)
    username = user.username

    if request.method == 'GET':
        return render_template('MyInformation.html',username=user.username, password=user.password, gender=user.gender, phoneNum=user.phoneNumber)

    # 处理POST请求
    newusername = request.form.get('user')
    newpwd = request.form.get('pwd')
    newgender = request.form.get('gender')
    newphoneNum = request.form.get('phoneNum')

    if newusername == '':
        flash('Username cannot be empty.')
        return render_template('MyInformation.html', username=user.username, password=user.password, gender=user.gender, phoneNum=user.phoneNumber)
    elif newpwd == '':
        flash('Password cannot be empty.')
        return render_template('MyInformation.html', username=user.username, password=user.password, gender=user.gender, phoneNum=user.phoneNumber)
    elif newgender == ' ':
        flash('Gender cannot be empty.')
        return render_template('MyInformation.html', username=user.username, password=user.password, gender=user.gender, phoneNum=user.phoneNumber)
    elif newphoneNum == '':
        flash('Phone Number cannot be empty.')
        return render_template('MyInformation.html', username=user.username, password=user.password, gender=user.gender, phoneNum=user.phoneNumber)




    # 创建连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='acthub')
    # 创建游标
    cursor = conn.cursor()
    sql_select = "SELECT username FROM user WHERE username='%s'" % (username)
    cursor.execute(sql_select)
    #result = cursor.fetchall()
    # 检查用户名是否需要更新
    if newusername != user.username: #更改用户名
        existing_user = User.query.filter_by(username=newusername).first() # 检查新用户名是否已存在
        if existing_user:
            flash('Username already taken.')
            return render_template('MyInformation.html', username=user.username, password=user.password, gender=user.gender, phoneNum=user.phoneNumber)
        user.username = newusername
        user.password = newpwd
        user.gender = newgender
        user.phoneNumber = newphoneNum
    else: #不改用户名
        user.password = newpwd
        user.gender = newgender
        user.phoneNumber = newphoneNum

    #new_user = User(username=newusername, password=pwd, gender=gender, phoneNumber=phoneNum)
    #db.session.add(new_user)
    db.session.commit()  # 提交事务，保存数据到数据库
    # db.session.close()  # 关闭会话，一般可以让Flask-SQLAlchemy自动管理会话
    return redirect('/MyInformation')

