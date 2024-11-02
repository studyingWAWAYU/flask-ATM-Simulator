from flask import render_template,request,redirect, flash,session
from flask import Blueprint

from ATMflask import db
from ATMflask.sql import User

lr = Blueprint('lr',__name__)

@lr.route('/Login',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def login():
    if request.method =='GET':
        return render_template('login.html')
    user = request.form.get('user')  # 获取POST传过来的值
    pwd = request.form.get('pwd')

    if user == '' or pwd == '':
        flash('User name and password can\'t be empty ')
        return render_template('login.html')

    clientlist = db.session.query(User).all()

    for client in clientlist:
        if user == client.username and client.password == pwd:
            session['id'] = client.id  # 用户信息放入session
            return redirect('/menu')

    else:
        flash('Invalid user name or password.')
        return render_template('login.html')


@lr.route('/Register',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def register():
    if request.method =='GET':
        return render_template('register.html')
    user = request.form.get('user')  # 获取POST传过来的值
    pwd = request.form.get('pwd')

    if user == '' or pwd == '':
        flash('用户名或密码不能为空')
        return render_template('login.html')

    clientlist = db.session.query(User).all()

    for client in clientlist:
        if user == client.username and client.password == pwd:
            session['id'] = client.id  # 用户信息放入session
            return redirect('/menu')

    else:
        flash('用户名或密码错误')
        return render_template('register.html')