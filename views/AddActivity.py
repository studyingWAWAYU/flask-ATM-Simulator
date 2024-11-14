import os.path

from flask import render_template,request,redirect, flash,session
from flask import Blueprint

from ATMflask import db
from ATMflask.sql import User
from ATMflask.sql import Membership
from ATMflask.sql import Club

addAct = Blueprint('addAct',__name__)

# 配置上传文件目录
#app.config['UPLOAD_FOLDER'] = 'static/img/uploads/'

@addAct.route('/AddActivity',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def addActivity():
    # 判断用户是否登录
    user_id = session.get('id')
    username = None
    myClubNameLST = None
    if user_id:
        user = User.query.get(user_id)
        username = user.username
        # 查询用户作为manager的所有社团，结果是列表嵌套元组，例如[(1,),(2,)]
        myClubId = db.session.query(Membership.club_id).filter_by(user_id=user_id,role='manager').all()
        if myClubId == []:
            flash("You are not the manager of any club, so you do not have permission to create a new activity.")
        else:
            myClubIdLST = [club_id[0] for club_id in myClubId]  # 把列表嵌套元组改为列表
            myClubName = db.session.query(Club.club_name).filter(Club.club_id.in_(myClubIdLST)).all()
            myClubNameLST = [club_name[0] for club_name in myClubName]
            print(myClubNameLST)

    if request.method == 'GET':
        return render_template('AddActivity.html',username=username,myClubNameLST=myClubNameLST)

    # 上传图片并保存
    if request.method == 'POST':
        file = request.files['photo']
        if file:
            file.save(os.path.join(os.getcwd(),'static/img/uploads',file.filename))
            # TODO:提取新activity的id，保存图片的路径为os.getcwd()+static/img/uploads/activity/ + id + filename

            return render_template('AddActivity.html')


