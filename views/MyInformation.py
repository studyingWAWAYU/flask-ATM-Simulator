from flask import render_template,request,redirect, flash,session
from flask import Blueprint

from ATMflask import db
from ATMflask.sql import User
import pymysql

myInfo = Blueprint('myInfo',__name__)

@myInfo.route('/MyInformation',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def myInformation():
    user_id = session.get('id')

    user = User.query.get(user_id)

    genderList = ["Female","Male","Non-binary"]

    if request.method == 'GET':
        return render_template('MyInformation.html',user=user,genderList=genderList)

    if request.method == 'POST':
        # 处理POST请求
        newusername = request.form.get('user')
        curpwd = request.form.get('curpwd')
        newpwd = request.form.get('pwd')
        newrepwd = request.form.get('repwd')
        newgender = request.form.get('gender')
        newphoneNum = request.form.get('phoneNum')
        avatarPath = request.form.get('selectedAvatar')

        if newusername == '':
            flash('Username cannot be empty.')
            return render_template('MyInformation.html', user=user,genderList=genderList)
        elif curpwd =='' or curpwd != user.password:
            flash('Current password is invalid.')
            return render_template('MyInformation.html', user=user,genderList=genderList)
        elif newpwd == '':
            flash('Password cannot be empty.')
            return render_template('MyInformation.html', user=user,genderList=genderList)
        elif newpwd != newrepwd:
            flash('Passwords do not match.')
            return render_template('MyInformation.html', user=user,genderList=genderList)
        elif newphoneNum == '':
            flash('Phone Number cannot be empty.')
            return render_template('MyInformation.html', user=user,genderList=genderList)


        # 检查用户名是否需要更新
        if newusername != user.username:  # 更改用户名
            existing_user = User.query.filter_by(username=newusername).one_or_none() # 检查新用户名是否已存在
            if existing_user:
                flash('Username already taken.')
                return render_template('MyInformation.html', user=user,genderList=genderList)
            else:
                user.username = newusername

        user.password = newpwd
        user.gender = newgender
        user.phoneNumber = newphoneNum
        user.avatar = avatarPath

        db.session.commit()  # 提交事务，保存数据到数据库
        # db.session.close()  # 关闭会话，一般可以让Flask-SQLAlchemy自动管理会话

        flash("Your information has been changed.")
        return render_template('MyInformation.html', user=user,genderList=genderList)

