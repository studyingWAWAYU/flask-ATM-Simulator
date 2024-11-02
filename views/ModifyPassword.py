from flask import render_template,request,flash,session
from flask import Blueprint

from ATMflask import db
from ATMflask.sql import User

MP = Blueprint('MP',__name__)

@MP.route('/ModifyPassword',methods = ['GET','POST'])#用装饰器定义路由的对应关系
def ModifyPassword():
    if request.method =='GET':
        return render_template('ModifyPassword.html')
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()
    pwd = request.form.get('pwd')
    newpwd = request.form.get('newpwd')
    confirmpwd = request.form.get('confirmpwd')

    if client.password == pwd and confirmpwd == newpwd:
        client.password = newpwd
        flash('修改成功!')
        return render_template('ModifyPassword.html')
    elif client.password != pwd:
        flash('原密码不正确')
        return render_template('ModifyPassword.html')
    elif confirmpwd != newpwd:
        flash('两次新密码输入不一致')
        return render_template('ModifyPassword.html')
    elif newpwd =='':
        flash('新密码不能为空')
        return render_template('ModifyPassword.html')
    else:
        flash('密码不正确，请重试')
        return render_template('ModifyPassword.html')
