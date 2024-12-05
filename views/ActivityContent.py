from flask import render_template,request,redirect, flash,session
from flask import Blueprint

import os
from ATMflask import db
from ATMflask.sql import User,Activity,Club,Participant

actct = Blueprint('actct',__name__)


@actct.route('/ActivityContent/<int:activity_id>',methods=['GET','POST'])
def activityContent(activity_id):
    user_id = session.get('id')
    session['activity_id'] = activity_id
    username = None
    actContent = None
    clubName = None
    par_status = None
    remaining = None
    isManager = False
    participants_dict = None
    isSignincode = None

    if user_id:
        user = User.query.get(user_id)
        username = user.username
        actContent = Activity.query.get(activity_id)

        ClubId = actContent.club_id
        clubName = db.session.query(Club.club_name).filter_by(club_id=ClubId).scalar()

        ActId = actContent.activity_id
        par_status = db.session.query(Participant.status).filter_by(user_id=user_id,activity_id=ActId).scalar()
        if par_status is None:
            par_status = "Sign up now"

        participant = db.session.query(Participant).filter_by(activity_id=ActId).filter(Participant.role != 'manager').all()
        # 剩余报名人数
        remaining = actContent.max_participant - len(participant)

        # 如果是manager就查询并显示用户列表
        par_role = db.session.query(Participant.role).filter_by(user_id=user_id,activity_id = actContent.activity_id).scalar()
        if par_role == "manager":
            isManager = True
            # 如果没有指定role，或role只有一种就按status分类显示
            if actContent.roles is None or ";" not in actContent.roles:
                status_dict = {}
                for p in participant:
                    status = p.status
                    if status not in status_dict:
                        status_dict[status] = []
                    user_name = db.session.query(User.username).filter_by(id = p.user_id).scalar()
                    status_dict[status].append(user_name)
                participants_dict = status_dict
            else:  # 如果有多个roles，就按roles分类显示
                roles_list = [roles.strip() for roles in actContent.roles.split(';')]
                role_dict = {role: [] for role in roles_list}
                for p in participant:
                    role = p.role
                    if role in role_dict:
                        user_name = db.session.query(User.username).filter_by(id=p.user_id).scalar()
                        role_dict[role].append(user_name + " (" + p.status + ")")
                participants_dict = role_dict
        if actContent.signin_code:
            isSignincode = True
        # 图片
        try:
            files = os.listdir(os.path.join(os.getcwd(), 'static', 'img', 'uploads', str(activity_id)))
            filelist = [f for f in files]
        except FileNotFoundError:
            filelist = None

    else:
        flash("Please login first to check all activities.")


    if request.method == 'GET':
        return render_template('ActivityContent.html',username=username,actContent=actContent,clubName=clubName,
                               par_status=par_status,remaining=remaining,isManager=isManager,participants_dict=participants_dict,filelist=filelist,isSignincode=isSignincode)
