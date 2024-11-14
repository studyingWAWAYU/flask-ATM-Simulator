from flask import render_template,request,redirect, flash,session
from flask import Blueprint

from ATMflask import db
from ATMflask.sql import User

actlb = Blueprint('actlb',__name__)

@actlb.route('/ActivityLobby',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def activityLobby():
    user_id = session.get('id')
    username = None

    if user_id:
        user = User.query.get(user_id)
        username = user.username

    if request.method == 'GET':
        return render_template('ActivityLobby.html',username=username)

@actlb.route('/ActivityContent',methods=['GET'])
def activityContent():
    if request.method == 'GET':
        return render_template('ActivityContent.html')
