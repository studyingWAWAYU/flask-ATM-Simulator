from flask import render_template,request,redirect, flash,session
from flask import Blueprint
from datetime import datetime
import pymysql

from ATMflask import db
from ATMflask.sql import User,Activity

actlb = Blueprint('actlb',__name__)

def parseDate(date_str):
    if date_str:
        return datetime.strptime(date_str, '%Y-%m-%d')
    return None

@actlb.route('/ActivityLobby',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def activityLobby():
    user_id = session.get('id')
    username = None
    Act = None

    if user_id:
        user = User.query.get(user_id)
        username = user.username

        ActId = db.session.query(Activity.activity_id).all()
        if ActId == []:
            flash("No activities have been created yet.")
        else:
            ActIdLst = [activity_id[0] for activity_id in ActId]  # 把列表嵌套元组改为列表
            Act = Activity.query.filter(Activity.activity_id.in_(ActIdLst)).all()

    if request.method == 'GET':
        return render_template('ActivityLobby.html',username=username,Act=Act)



@actlb.route('/GetActivity', methods=['GET','POST'])
def getActivity(type=None, status=None, signup_start=None, signup_end=None, start_time=None, end_time=None):
    type = request.form.get('type')
    status = request.form.get('status')
    signup_start = request.form.get('signup_start')
    signup_end = request.form.get('signup_end')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')

    query = db.Activity.query()
    signup_start = parseDate(signup_start)
    signup_end = parseDate(signup_end)
    start_time = parseDate(start_time)
    end_time = parseDate(end_time)

    if type:
        query = query.filter(db.Activity.type == type)
    if status:
        query = query.filter(db.Activity.status == status)
    if signup_start:
        query = query.filter(db.Activity.signup_start >= signup_start)
    if signup_end:
        query = query.filter(db.Activity.signup_end <= signup_end)
    if start_time:
        query = query.filter(db.Activity.start_time >= start_time)
    if end_time:
        query = query.filter(db.Activity.end_time <= end_time)

    # 执行查询并返回结果
    activities = query.all()
    return render_template('ActivityLobby.html', activities=activities)

    #创建连接
    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='acthub')
    #创建游标
    # cursor = conn.cursor()

'''
# 搜索功能，还没写完
@actlb.route('/Search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        act_name = db.search("select * from activity_name")
        return render_template('ActivityLobby.html')
'''