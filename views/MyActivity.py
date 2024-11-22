from flask import render_template,request,redirect, flash,session
from flask import Blueprint

from ATMflask import db
from ATMflask.sql import User,Participant,Activity,Membership

myAct = Blueprint('myAct',__name__)

@myAct.route('/MyActivity',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def MyActivity():
    user_id = session.get('id')
    username = None
    myAct = None
    createPermission = False

    if user_id:
        user = User.query.get(user_id)
        username = user.username

        # 查询用户作为manager的所有社团
        myClubId = db.session.query(Membership.club_id).filter_by(user_id=user_id, role='manager').all()
        if myClubId != []:  # 如果用户是某社团的manager，就可以create new activity
            createPermission = True

        myActId = db.session.query(Participant.activity_id).filter_by(user_id=user_id).all()
        if myActId == []:
            flash("You haven't participated in any activity.")
        else:
            myActIdLST = [activity_id[0] for activity_id in myActId]  # 把列表嵌套元组改为列表
            myAct = Activity.query.filter(Activity.activity_id.in_(myActIdLST)).all()
            #print(myAct)

    else:
        flash("Please login first to check your activities.")

    if request.method == 'GET':
        return render_template('MyActivity.html',username=username,myAct=myAct,createPermission=createPermission)