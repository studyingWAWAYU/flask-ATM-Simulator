from datetime import datetime
import time
from flask import render_template, request, flash, session, Blueprint, jsonify
from ATMflask import db
from ATMflask.sql import User, Participant, Activity

# 定义 Blueprint，用于模块化管理活动相关的路由
parManage = Blueprint('parManage', __name__)

# 报名活动的路由
@parManage.route('/applyAct', methods=['POST'])
def apply_act():
    data = request.get_json()
    user_id = data.get('userId')  # 获取用户 ID
    act_id = data.get('activityId')  # 获取活动 ID

    if not act_id:
        return jsonify({'success': False, 'message': 'Activity ID is required.'})

    if not user_id:
        return jsonify({'success': False, 'message': 'User ID is required.'})

    # 获取活动信息
    activity = Activity.query.get(act_id)
    if not activity:
        return jsonify({'success': False, 'message': 'Activity not found.'})

    # 检查活动是否已满
    current_participants = Participant.query.filter_by(activity_id=act_id,role="participant").all()
    if len(current_participants) >= activity.max_participant:
        return jsonify({'success': False, 'message': 'Activity is already full.'})

    # 检查用户是否已经报名
    existing_participant = Participant.query.filter_by(user_id=user_id,activity_id=act_id).first()
    if existing_participant:
        return jsonify({'success': False, 'message': 'You are already signed up for this activity.'})

    # 创建新报名记录
    new_participant = Participant(user_id=user_id,activity_id=act_id,status="Registered",role="participant")
    db.session.add(new_participant)
    db.session.commit()

    # 更新剩余名额
    remaining = activity.max_participant - len(current_participants) - 1
    db.session.commit()

    return jsonify({'success': True, 'remaining': remaining})


# 管理活动的路由
@parManage.route('/ParticipantsManage/<int:activity_id>', methods=['GET', 'POST'])
def manage_act(activity_id):
    # 获取活动 ID
    activity_id = activity_id
    session['activity_id'] = activity_id

    # 获取当前用户信息
    user_id = session.get('id')
    username = db.session.query(User.username).filter_by(id=user_id).scalar()
    par_role = db.session.query(Participant.role).filter_by(user_id=user_id,activity_id=activity_id).scalar()

    if request.method == 'GET':  # 显示参与者列表
        participants = db.session.query(Participant).filter_by(activity_id=activity_id).all()

        participant_details = []
        for p in participants:
            if p.role != 'manager' or par_role != 'manager':
                userId = p.user_id
                user_name = db.session.query(User).filter_by(id=userId).first().username
                user_gender = db.session.query(User).filter_by(id=userId).first().gender
                user_phone_number = db.session.query(User).filter_by(id=userId).first().phoneNumber
                participant_details.append({
                    'user_id': p.user_id,
                    'status': p.status,
                    'role': p.role,
                    'user_name': user_name if user_name else 'N/A',
                    'user_gender': user_gender if user_gender else 'N/A',
                    'user_phone_number': user_phone_number if user_phone_number else 'N/A'})
        return render_template('ParticipantsManage.html',username=username,participants=participant_details,activity_id=activity_id)
#删除参与者
@parManage.route('/deleteParticipant', methods=['POST'])
def delete_participant():
        data = request.get_json()
        user_id = data.get('user_id')
        activity_id = session.get('activity_id')

        if request.method == 'POST':
            participant = db.session.query(Participant).filter_by(user_id=user_id,activity_id=activity_id).first()
            if participant:
                db.session.delete(participant)
                db.session.commit()
        return jsonify({"message": "Participant deleted successfully!"})

# 更新参与者状态
@parManage.route('/updateStatus', methods=['POST'])
def update_status():
    data = request.get_json()
    user_id = data.get('user_id')
    status = data.get('status')
    activity_id = session.get('activity_id')

    if request.method == 'POST':
        participant = db.session.query(Participant).filter_by(user_id=user_id,activity_id=activity_id).first()
        if participant:
            participant.status = status
            db.session.commit()
        return jsonify({"message": "Status updated successfully!"})

# 增加参与者
@parManage.route('/addParticipant', methods=['POST'])
def add_participant():
    data = request.get_json()
    user_id = data.get('user_id')
    activity_id = session.get('activity_id')

    # 检查用户是否存在
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404  # 返回错误信息，用户未找到

    if request.method == 'POST':
        activity = db.session.query(Activity).filter_by(activity_id=activity_id).first()
        participant = db.session.query(Participant).filter_by(user_id=user_id,activity_id=activity_id).first()
        current_participants = Participant.query.filter_by(activity_id=activity_id,role="participant" ).all()
        if participant:
            return jsonify({'error': 'User is already signed up for this activity.'})
        elif len(current_participants) >= activity.max_participant:
            return jsonify({'error': 'Activity is already full.'})
        else:
            new_participant = Participant(user_id=user_id,activity_id=activity_id,status="Registered",role="participant")
            db.session.add(new_participant)
            db.session.commit()

        return jsonify({"message": "Participant added successfully!"})

# 发布签到码
@parManage.route('/postSigninCode', methods=['POST'])
def post_signin_code():
    if request.method == 'POST':
        data = request.get_json()  # 获取前端发送的 JSON 数据
        activity_id = session.get('activity_id')  # 获取活动 ID
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
@parManage.route('/signin', methods=['POST'])
def signin():
    user_id = session.get('id')
    activity_id = session.get('activity_id')

    if request.method == 'POST':  # 提交签到
        data = request.get_json()
        new_signin_code = data.get('new_signin_code')
        signin_code = db.session.query(Activity.signin_code).filter_by(activity_id=activity_id).scalar()
        activity = db.session.query(Activity).filter_by(activity_id=activity_id).first()
        if not activity:
            # 如果活动不存在，返回 404 错误
            return jsonify({'error': 'Activity not found.'}), 404
        # 校验活动时间范围
        timestamp = time.time()
        dt_object = datetime.fromtimestamp(timestamp)
        formatted_time_str = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        formatted_time = datetime.strptime(formatted_time_str, '%Y-%m-%d %H:%M:%S')
        start_time = activity.start_time
        end_time = activity.end_time


        if start_time >= formatted_time:
            return jsonify({'error': 'This activity has not started yet.'}), 400
        if end_time <= formatted_time:
            participant = db.session.query(Participant).filter_by(user_id=user_id,activity_id=activity_id).first()
            if participant:
                participant.status = 'Absent'
                db.session.commit()
                return jsonify({'error': 'You missed the sign-in time.'}), 400  # 返回错误信息

        # 校验签到码
        if new_signin_code != signin_code:
            return jsonify({'error': 'Incorrect sign-in code.'}), 400  # 返回错误信息

        # 签到成功：更新参与者状态
        participant = db.session.query(Participant).filter_by(user_id=user_id,activity_id=activity_id).first()
        if participant:
            participant.status = 'Present'
            db.session.commit()
            return jsonify({'message': 'Sign-in successfully!'})