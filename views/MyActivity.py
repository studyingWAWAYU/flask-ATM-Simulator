from flask import render_template,request,redirect, flash,session
from flask import Blueprint

from ATMflask import db
from ATMflask.sql import User

myAct = Blueprint('myAct',__name__)

@myAct.route('/MyActivity',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def MyActivity():
    user_id = session.get('id')
    username = None

    if user_id:
        user = User.query.get(user_id)
        username = user.username

    if request.method == 'GET':
        return render_template('MyActivity.html',username=username)