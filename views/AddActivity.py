import os.path

from flask import render_template,request,redirect, flash,session
from flask import Blueprint

from ATMflask import db
from ATMflask.sql import User

addAct = Blueprint('addAct',__name__)

# 配置上传文件目录
#app.config['UPLOAD_FOLDER'] = 'static/img/uploads/'

@addAct.route('/AddActivity',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def addActivity():
    # 判断用户是否登录
    user_id = session.get('id')
    username = None
    if user_id:
        user = User.query.get(user_id)
        username = user.username
        # 查询用户是否有manager身份
        myClubId = user.MyClubId
        print(myClubId)

    if request.method == 'GET':
        return render_template('AddActivity.html',username=username)


    # 上传图片并保存
    if request.method == 'POST':
        file = request.files['photo']
        if file:
            file.save(os.path.join(os.getcwd(),'static/img/uploads',file.filename))
            # TODO:提取新activity的id，保存图片的路径为os.getcwd()+static/img/uploads/activity/ + id + filename

            return render_template('AddActivity.html',username=username)


