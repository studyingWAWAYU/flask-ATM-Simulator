from flask import render_template,request,redirect, flash,session
from flask import Blueprint
from datetime import datetime

from ATMflask import db
from ATMflask.sql import User, Participant, Activity, Membership, Club

myAct = Blueprint('myAct',__name__)

def update_status(act):
    current = datetime.now()
    if act.end_time < current:
        return 'Completed'
    elif act.start_time <= current <= act.end_time:
        return 'Ongoing'
    else:
        return 'Upcoming'

@myAct.route('/MyActivity',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def MyActivity():
    user_id = session.get('id')
    username = None
    myAct = None
    createPermission = False
    selected_acts = None
    clubNames = {}
    remainings = {}

    if user_id:
        user = User.query.get(user_id)
        username = user.username
        myActIdLST = []

        # 查询用户作为manager的所有社团
        myClubId = db.session.query(Membership.club_id).filter_by(user_id=user_id, role='manager').all()
        if myClubId != []:
            createPermission = True  # 如果用户是某社团的manager，就可以create new activity

            # 查询用户管理的社团
            for eachClubId in myClubId:
                manage_ActId = db.session.query(Activity.activity_id).filter_by(club_id=eachClubId[0]).all()
                if manage_ActId:
                    manage_ActIdLST = [activity_id[0] for activity_id in manage_ActId]
                    myActIdLST.extend(manage_ActIdLST)
        # 查询用户参与的社团
        par_ActId = db.session.query(Participant.activity_id).filter_by(user_id=user_id).all()
        if par_ActId:
            par_ActIdLST = [activity_id[0] for activity_id in par_ActId]
            myActIdLST.extend(par_ActIdLST)

        if myActIdLST == []:
            flash("You haven't participated in any activity.")
        else:
            myAct = Activity.query.filter(Activity.activity_id.in_(myActIdLST)).all()

            for act in myAct:
                act.status = update_status(act)
                ClubId = act.club_id
                clubName = db.session.query(Club.club_name).filter_by(club_id=ClubId).scalar()
                clubNames[act.activity_id] = clubName

                eachActId = act.activity_id
                participant = db.session.query(Participant).filter_by(activity_id=eachActId).filter(
                    Participant.role != 'manager').all()
                # 剩余报名人数
                remainings[act.activity_id] = act.max_participant - len(participant)

        if request.method == 'POST':
            search_word = request.form.get('search-input')
            if search_word:
                selected_acts = [act for act in myAct if search_word.lower() in act.activity_name.lower()]
                if not selected_acts:
                    flash("No matching activities were found yet. All activities are displayed below.")
            else:
                selected_acts = myAct
            return render_template('MyActivity.html', username=username, myAct=myAct, createPermission=createPermission,
                                   clubNames=clubNames, selected_acts=selected_acts, remainings=remainings)

    else:
        flash("Please login first to check your activities.")

    if request.method == 'GET':
        return render_template('MyActivity.html',username=username,myAct=myAct,createPermission=createPermission,
                               clubNames=clubNames,selected_acts=selected_acts,remainings=remainings)