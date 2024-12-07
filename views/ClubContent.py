from flask import render_template, request, redirect, flash, session, url_for, jsonify
from flask import Blueprint

from ATMflask import db
from ATMflask.sql import User, Participant, Activity, Membership, Club
from datetime import datetime

clubct = Blueprint('clubct', __name__)

# 获取社团成员列表
def get_club_members(club_id):
    # 获取社团
    club = db.session.query(Club).get(club_id)
    if not club:
        return None  # 如果没有找到社团，返回None

    # 查询该社团的所有成员
    members = db.session.query(User).join(Membership).filter(Membership.club_id == club_id).all()

    return members

@clubct.route('/ClubContent/<int:club_id>', methods=['GET', 'POST'])
def clubContent(club_id):
    user_id = session.get('id')
    username = None
    is_manager = False
    ifjoined = False

    if user_id:
        user = User.query.get(user_id)
        username = user.username

        # 获取该社团的信息
        club = db.session.query(Club).get(club_id)
        # 获取该社团的成员列表
        members = get_club_members(club_id)
        # 获取该社团的成员数量
        num_members = db.session.query(Membership).filter(Membership.club_id == club.club_id).count()
        # 获取社团的经理
        manager = db.session.query(User).join(Membership).filter(Membership.club_id == club.club_id,Membership.role == 'manager').first()

        # 判断当前用户是否为该社团的manager
        if manager and manager.id == user_id:
            is_manager = True

        for member in members:
            if member.id == user_id:
                ifjoined = True
                break

        # 返回模板并传递数据
        return render_template('ClubContent.html', club=club, manager=manager, num_members=num_members,
                               is_manager=is_manager, members=members,username=username, ifjoined = ifjoined)
    else:  # 如果用户没有登录
        flash('You must log in first to view the club details.')
        return redirect('/ClubLobby')

@clubct.route('/EditClub/<int:club_id>', methods=['GET', 'POST'])
def editClub(club_id):
    # 获取当前登录的用户
    user_id = session.get('id')
    user = User.query.get(user_id)
    username = user.username

    # 获取该社团的信息
    club = db.session.query(Club).get(club_id)
    manager = db.session.query(User).join(Membership).filter(Membership.club_id == club.club_id,
                                                             Membership.role == 'manager').first()

    # 获取当前登录的用户
    user_id = session.get('id')
    is_manager = False

    if user_id:
        # 检查当前用户是否是社团的负责人 (manager)
        if manager and manager.id == user_id:
            is_manager = True

    if request.method == 'POST':
        # 获取用户提交的表单数据
        club_name = request.form.get('club_name')
        description = request.form.get('description')

        # 更新社团信息
        club.club_name = club_name
        club.description = description

        try:
            # 提交更新
            db.session.commit()
            flash('Club updated successfully!', 'success')
            return redirect(url_for('clubct.clubContent', club_id=club_id))
        except Exception as e:
            db.session.rollback()
            flash('Error updating club. Please try again.', 'danger')

    # 如果是GET请求，则渲染编辑表单
    return render_template('editClub.html', club=club,is_manager=is_manager,username=username)


@clubct.route('/DeleteClub/<int:club_id>', methods=['GET'])
def deleteClub(club_id):
    # 获取社团信息
    club = Club.query.get(club_id)

    if not club:
        flash("Club not found.", "error")
        return redirect(url_for('clublb.clublobby'))  # 如果社团不存在，重定向到社团列表

    # 检查当前用户是否为社团经理
    user_id = session.get('id')
    if not user_id:
        flash("Please log in to delete a club.", "error")
        return redirect(url_for('auth.login'))  # 如果未登录，重定向到登录页

    # 获取该社团的经理
    manager = db.session.query(User).join(Membership).filter(Membership.club_id == club_id,
                                                             Membership.role == 'manager').first()

    if not manager or manager.id != user_id:
        flash("You are not authorized to delete this club.", "error")
        return redirect(url_for('clublb.clublobby'))  # 如果当前用户不是社团经理，重定向到社团列表

    # 删除社团及其相关信息
    try:
        # 删除活动关联（如果有）
        Activities = Activity.query.filter_by(club_id = club_id).all()
        print(Activities)
        if Activities:
            for eachActivity in Activities:
                # 删除关联活动的participants
                current_participants = Participant.query.filter_by(activity_id=eachActivity.activity_id).all()
                print(current_participants)
                if current_participants:
                    for each_participant in current_participants:
                        db.session.delete(each_participant)
                    db.session.commit()
                db.session.delete(eachActivity)

        # 删除社团成员关系
        db.session.query(Membership).filter_by(club_id = club_id).delete()
        db.session.commit()
        # 删除社团
        db.session.delete(club)
        db.session.commit()
        flash(f"Club {club.club_name} has been deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while deleting the club: {str(e)}", "error")

    return redirect(url_for('clublb.clublobby'))  # 删除后重定向到社团列表


# Release Announcement 页面
@clubct.route('/ReleaseAnnoucement/<int:club_id>', methods=['GET', 'POST'])
def releaseAnnouncement(club_id):
    # 获取当前登录的用户
    user_id = session.get('id')
    user = User.query.get(user_id)
    username = user.username

    club = db.session.query(Club).get(club_id)

    if not club:
        return "Club not found", 404

    # 返回模板，传递社团信息
    if request.method == 'POST':
        # 获取公告内容
        announcement_content = request.form['announcement']

    if request.method == 'POST':
        # 获取用户提交的公告内容
        announcement_content = request.form.get('announcement')

        if announcement_content:
            # 更新社团的公告字段
            club.announcement = announcement_content
            db.session.commit()  # 提交更改到数据库

            flash('Announcement successfully released!', 'success')  # 显示成功信息
            return redirect(url_for('clubct.clubContent', club_id=club_id))  # 重定向到该社团的详情页面

    return render_template('ReleaseAnnoucement.html', club_name=club.club_name, club_id=club_id,club=club,username=username)

@clubct.route('/ClubMemberManage/<int:club_id>', methods=['GET', 'POST'])
def manageMemberList(club_id):
    # 获取当前登录的用户
    user_id = session.get('id')
    user = User.query.get(user_id)
    username = user.username

    # 获取该社团的成员列表
    members = get_club_members(club_id)

    return render_template('ClubMemberManage.html', club_id=club_id,members=members,username=username)

@clubct.route('/addClubMember', methods=['POST'])
def addClubMember():
    data = request.get_json()
    user_id = data.get('user_id')
    club_id = data.get('club_id')

    # 检查用户是否存在
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404  # 返回错误信息，用户未找到

    if request.method == 'POST':
        # 增加成员
        existing_member = Membership.query.filter_by(club_id=club_id, user_id=user_id).first()
        if existing_member:
            return jsonify({'error':'User is already a member of this club!'}),409
        else:
            new_member = Membership(club_id=club_id, user_id=user_id, role='member')
            db.session.add(new_member)
            db.session.commit()
            return jsonify({'message':'Member added successfully!'}),201

@clubct.route('/deleteClubMember', methods=['POST'])
def deleteClubMember():
        data = request.get_json()
        user_id = data.get('user_id')
        club_id = data.get('club_id')

        if request.method == 'POST':
            member = db.session.query(Membership).filter_by(user_id=user_id,club_id=club_id).first()
            if member is not None:
                db.session.delete(member)
                db.session.commit()
        return jsonify({"message": "Member is deleted successfully!"})


@clubct.route('/joinClub/<int:club_id>', methods=['POST','GET'])
def joinClub(club_id):
    # 获取当前登录的用户
    user_id = session.get('id')

    if user_id:
        current_time = datetime.now()
        nowTime = current_time.strftime('%Y-%m-%dT%H:%M')

        # 添加用户到俱乐部
        new_member = Membership(club_id=club_id, user_id=user_id, role="member",join_time = nowTime)
        db.session.add(new_member)
        db.session.commit()

        return redirect("/ClubContent/"+str(club_id))


@clubct.route('/quitClub/<int:club_id>', methods=['POST','GET'])
def quitClub(club_id):
    # 获取当前登录的用户
    user_id = session.get('id')

    if user_id:
        # 在俱乐部里删除用户
        current_member = Membership.query.filter_by(user_id = user_id, club_id=club_id).first()
        db.session.delete(current_member)
        db.session.commit()

        return redirect("/ClubContent/"+str(club_id))