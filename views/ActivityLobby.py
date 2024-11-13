from flask import render_template,request,redirect, flash,session
from flask import Blueprint

from ATMflask import db
#from ATMflask.sql import User

actlb = Blueprint('actlb',__name__)

@actlb.route('/ActivityLobby',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def activityLobby():
    if request.method == 'GET':
        return render_template('ActivityLobby.html')