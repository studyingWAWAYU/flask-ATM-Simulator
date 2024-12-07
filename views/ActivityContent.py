from datetime import datetime
from flask import render_template, request, redirect, flash, session, jsonify
from flask import Blueprint

import os
from ATMflask import db
from ATMflask.sql import User,Activity,Club,Participant,Membership

actct = Blueprint('actct',__name__)

def update_status(act):
    current = datetime.now()
    if act.end_time < current:
        return 'Completed'
    elif act.start_time <= current <= act.end_time:
        return 'Ongoing'
    else:
        return 'Upcoming'

@actct.route('/ActivityContent/<int:activity_id>',methods=['GET','POST'])
def activityContent(activity_id):
    user_id = session.get('id')
    username = None
    actContent = None
    clubName = None
    par_status = None
    remaining = None
    isManager = False
    participants_dict = None
    filelist = None
    isSignup = False

    if user_id:
        user = User.query.get(user_id)
        username = user.username
        actContent = Activity.query.get(activity_id)

        actContent.status = update_status(actContent)

        ClubId = actContent.club_id
        clubName = db.session.query(Club.club_name).filter_by(club_id=ClubId).scalar()

        ActId = actContent.activity_id
        par_status = db.session.query(Participant.status).filter_by(user_id=user_id,activity_id=ActId).scalar()
        if par_status is None:
            par_status = "Sign up now"

        participant = db.session.query(Participant).filter_by(activity_id=ActId).all()
        # 剩余报名人数
        remaining = actContent.max_participant - len(participant)

        # 如果用户是活动属于club的manager就查询并显示用户列表
        club_role = db.session.query(Membership.role).filter_by(user_id=user_id,club_id=ClubId).scalar()
        if club_role == "manager":
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

        # 图片
        files = os.listdir(os.path.join(os.getcwd(), 'static', 'img', 'uploads', str(activity_id)))
        filelist = [f for f in files]

        # 报名时间
        current = datetime.now()
        if actContent.signup_start <= current <= actContent.signup_end:
            isSignup = True

    else:
        flash("Please login first to check all activities.")
        redirect('ActivityLobby')

    if request.method == 'GET':
        return render_template('ActivityContent.html',username=username,actContent=actContent,clubName=clubName,par_status=par_status,
                               remaining=remaining,isManager=isManager,participants_dict=participants_dict,filelist=filelist,isSignup=isSignup)

# 报名活动
@actct.route('/Signup', methods=['POST'])
def signup():
    user_id = session.get('id')
    data = request.get_json()
    act_id = data.get('activity_id')  # 获取活动 ID

    # 获取活动信息
    activity = Activity.query.get(act_id)
    if not activity:
        return jsonify({'success': False, 'message': 'Activity not found.'})

    # 检查活动是否已满
    current_participants = Participant.query.filter_by(activity_id=act_id).all()
    if len(current_participants) >= activity.max_participant:
        return jsonify({'success': False, 'message': 'Activity is already full.'})

    # 检查用户是否已经报名
    existing_participant = Participant.query.filter_by(user_id=user_id,activity_id=act_id).first()
    if existing_participant:
        return jsonify({'success': False, 'message': 'You have signed up for this activity before.'})

    # 创建新报名记录
    new_participant = Participant(user_id=user_id,activity_id=act_id,status="Registered")
    db.session.add(new_participant)
    db.session.commit()

    # 更新剩余名额
    remaining = activity.max_participant - len(current_participants) - 1
    db.session.commit()

    return jsonify({'success': True, 'remaining': remaining})

# 发布签到码
@actct.route('/postSigninCode/<int:activity_id>', methods=['POST'])
def post_signin_code(activity_id):
    if request.method == 'POST':
        data = request.get_json()  # 获取前端发送的 JSON 数据
        signin_code = data.get('signin_code')  # 获取签到码

        # 将签到码存入活动信息
        activity = db.session.query(Activity).filter_by(activity_id=activity_id).first()
        if activity:
            activity.signin_code = signin_code
            db.session.commit()
            flash("Sign in code posted successfully.")
            return jsonify({'message': 'Sign-in code posted successfully!'})  # 返回成功信息
        else:
            return jsonify({'error': 'Activity ID not found.'}), 400  # 返回错误信息

# 签到
@actct.route('/signin/<int:activity_id>', methods=['POST'])
def signin(activity_id):
    user_id = session.get('id')

    if request.method == 'POST':  # 提交签到
        data = request.get_json()
        new_signin_code = data.get('new_signin_code')
        signin_code = db.session.query(Activity.signin_code).filter_by(activity_id=activity_id).scalar()

        # 校验签到码
        if new_signin_code != signin_code:
            return jsonify({'error': 'Incorrect sign-in code.'}), 400  # 返回错误信息

        # 签到成功：更新参与者状态
        participant = db.session.query(Participant).filter_by(user_id=user_id,activity_id=activity_id).first()
        if participant:
            participant.status = 'Present'
            db.session.commit()
            return jsonify({'message': 'Sign-in successfully!'})