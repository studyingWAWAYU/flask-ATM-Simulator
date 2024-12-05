# 登录和注册功能
from flask import render_template,request,redirect, flash,session
from flask import Blueprint

from ATMflask import db
from ATMflask.sql import User
import pymysql

auth = Blueprint('auth',__name__)

@auth.route('/Login',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def login():
    if request.method =='GET':
        return render_template('login.html')
    user = request.form.get('user')  # 获取POST传过来的值
    pwd = request.form.get('pwd')

    if user == '' or pwd == '':
        flash('User name or password cannot be empty ')
        return render_template('login.html')

    clientlist = db.session.query(User.id,User.username,User.password).all()

    for client in clientlist:
        if user == client.username and client.password == pwd:
            session['id'] = client.id  # 用户信息放入session
            return redirect('/')

    else:
        flash('Invalid user name or password.')
        return render_template('login.html')


@auth.route('/Register',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def register():
    if request.method =='GET':
        return render_template('register.html')
    user = request.form.get('user')  # 获取POST传过来的值
    pwd = request.form.get('pwd')
    repwd = request.form.get('repwd')
    phoneNum = request.form.get('phoneNum')

    if user == '':
        flash('Username cannot be empty.')
        return render_template('register.html')
    elif len(user)>20:
        flash('The username length cannot exceed 20 characters.')
    elif pwd == '':
        flash('Password cannot be empty.')
        return render_template('register.html')
    elif pwd != repwd:
        flash('Passwords do not match.')
        return render_template('register.html')
    elif phoneNum == '':
        flash('Phone Number cannot be empty.')
        return render_template('register.html')

    # 创建连接
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='root',db='acthub')
    # 创建游标
    cursor = conn.cursor()

    sql_select = "SELECT username FROM user WHERE username='%s'" %(user)
    cursor.execute(sql_select)
    result = cursor.fetchall()
    if (len(result)==0):
        new_user = User(username=user,password=pwd,phoneNumber=phoneNum)
        db.session.add(new_user)
        db.session.commit()  # 提交事务，保存数据到数据库
        #db.session.close()  # 关闭会话，一般可以让Flask-SQLAlchemy自动管理会话
        return redirect('/Login')
    else:
        flash('This username is already taken.')
        return render_template('register.html')

@auth.route('/Logout', methods = ['GET','POST'])
def logout():
    session.pop('id', None)  # 清除session中的用户ID
    return redirect('/')