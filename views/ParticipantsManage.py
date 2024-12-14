from datetime import datetime
import time
from flask import render_template, request, flash, session, Blueprint, jsonify
from ATMflask import db
from ATMflask.sql import User, Participant, Activity

parManage = Blueprint('parManage', __name__)

@parManage.route('/ParticipantsManage/<int:activity_id>', methods=['GET', 'POST'])
def manage_act(activity_id):
    # 获取当前用户信息
    user_id = session.get('id')
    username = db.session.query(User.username).filter_by(id=user_id).scalar()

    if request.method == 'GET':  # 显示参与者列表
        participants = db.session.query(Participant).filter_by(activity_id=activity_id).all()

        participant_details = []
        for p in participants:
            userId = p.user_id
            user_name = db.session.query(User).filter_by(id=userId).first().username
            user_gender = db.session.query(User).filter_by(id=userId).first().gender
            user_phone_number = db.session.query(User).filter_by(id=userId).first().phoneNumber
            participant_details.append({
                'user_id': p.user_id,
                'status': p.status,
                'role': p.role if p.role else 'N/A',
                'user_name': user_name,
                'user_gender': user_gender if user_gender else 'N/A',
                'user_phone_number': user_phone_number})
        return render_template('ParticipantsManage.html',username=username,participants=participant_details,activity_id=activity_id)

# 删除参与者
@parManage.route('/deleteParticipant', methods=['POST'])
def delete_participant():
        data = request.get_json()
        user_id = data.get('user_id')
        activity_id = data.get('activityId')

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
    activity_id = data.get('activity_id')

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
    activity_id = data.get('activityId')

    # 检查用户是否存在
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404  # 返回错误信息，用户未找到

    if request.method == 'POST':
        activity = db.session.query(Activity).filter_by(activity_id=activity_id).first()
        participant = db.session.query(Participant).filter_by(user_id=user_id,activity_id=activity_id).first()
        current_participants = Participant.query.filter_by(activity_id=activity_id).all()
        if participant:
            return jsonify({'error': 'User is already signed up for this activity.'})
        elif len(current_participants) >= activity.max_participant:
            return jsonify({'error': 'Activity is already full.'})
        else:
            new_participant = Participant(user_id=user_id,activity_id=activity_id,status="Registered")
            db.session.add(new_participant)
            db.session.commit()

        return jsonify({"message": "Participant added successfully!"})