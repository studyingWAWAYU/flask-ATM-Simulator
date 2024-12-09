from datetime import datetime

from flask import render_template, request, redirect, flash, session, url_for, jsonify
from flask import Blueprint

from ATMflask import db
from ATMflask.sql import User,Club,Membership

clublb = Blueprint('clublb', __name__)

# 显示所有社团
@clublb.route('/ClubLobby', methods=['post', 'get'])
def clublobby():
    user_id = session.get('id')
    username = None
    #----------------- 所有用户部分 -------------------#
    search_query = request.args.get('search')  # 获取搜索关键词
    # 获取所有社团并计算每个社团的成员人数和manager
    all_clubs_data = []

    if search_query:
        # 如果有搜索关键词，按关键词过滤社团
        all_clubs = db.session.query(Club).filter(Club.club_name.like(f"%{search_query}%")).all()
    else:
        all_clubs = db.session.query(Club).all()

    for club in all_clubs:
        # 获取该俱乐部的成员数量
        num_members = db.session.query(Membership).filter(Membership.club_id == club.club_id).count()

        # 获取该俱乐部的经理（假设role = "manager"）
        manager = db.session.query(User).join(Membership).filter(Membership.club_id == club.club_id,
                                                                 Membership.role == "manager").first()

        # 将结果存储为元组： (Club对象, manager, num_members)
        all_clubs_data.append((club, manager, num_members))
        # 获取所有社团及其成员数量
        club_data = db.session.query(
            Club.club_name,
            db.func.count(Membership.user_id).label('member_count')
        ).join(Membership, Club.club_id == Membership.club_id) \
            .group_by(Club.club_name) \
            .order_by(db.func.count(Membership.user_id).desc()) \
            .limit(10).all()  # 获取成员最多的前10个社团

        # 将俱乐部名称和成员数量分别存储
        club_names = [club.club_name for club in club_data]
        member_counts = [club.member_count for club in club_data]

    # ----------------- 当前登录用户部分 -------------------#
    club_details = []

    if user_id:
        user = User.query.get(user_id)
        username = user.username

        # 获取当前用户参与的社团，包括社团、用户角色
        user_clubs = db.session.query(Club, Membership.role).join(Membership).filter(
            Membership.user_id == user_id).all()

        # 获取每个社团的 manager 和成员人数

        for club, role in user_clubs:
            # 获取社团的经理（role="manager"）
            manager = db.session.query(User.username).join(Membership).filter(Membership.club_id == club.club_id,
                                                                              Membership.role == 'manager').first()

            # 获取社团的成员人数
            member_count = db.session.query(Membership).filter(Membership.club_id == club.club_id).count()

            # 将社团、经理和成员人数打包成一个元组，存储到club_details中
            club_details.append((club, manager.username if manager else None, member_count))

    # ---------------- Echarts -------------------#
    # 获取每个俱乐部的名称和成员数量
    club_data = db.session.query(Club.club_name, db.func.count(Membership.user_id).label('member_count')) \
        .join(Membership, Club.club_id == Membership.club_id) \
        .group_by(Club.club_id) \
        .order_by(db.func.count(Membership.user_id).desc()) \
        .limit(10)  # 只取前10个俱乐部

    # 提取俱乐部名称和成员数量
    clubs = [{'club_name': club.club_name, 'member_count': club.member_count} for club in club_data]

    # 分别提取俱乐部名称和成员数量
    club_names = [club['club_name'] for club in clubs]
    member_counts = [club['member_count'] for club in clubs]

    return render_template('ClubLobby.html', user_clubs=club_details, clubs=all_clubs_data,user_id=user_id,username=username,club_names=club_names,member_counts=member_counts)

@clublb.route('/CreateClub', methods=['GET', 'POST'])
def createClub():
    # 获取当前用户的ID
    user_id = session.get('id')

    if not user_id:
        flash('You must log in first to create a club.', 'error')
        return redirect('/ClubLobby')

    user = User.query.get(user_id)
    username = user.username
    if request.method == 'POST':
        # 获取用户提交的数据
        club_name = request.form.get('club_name')
        description = request.form.get('description')

        #判断club name不能重复
        clubName_exists = Club.query.filter_by(club_name=club_name).first()
        if clubName_exists:
            flash("This club name already exists.")
            return render_template('CreateClub.html', username=username)

        if club_name and description:
            # 创建新的俱乐部对象
            current_time = datetime.now()
            new_club = Club(club_name=club_name, description=description,created_time=current_time)
            db.session.add(new_club)
            db.session.commit()

            # 获取新创建的俱乐部ID
            club_id = new_club.club_id

            # 创建该社团的经理和成员关系
            membership = Membership(user_id=user_id, club_id=club_id, role='manager')
            db.session.add(membership)
            db.session.commit()

            # 提示用户社团创建成功
            flash('Club created successfully!', 'success')
            return redirect(url_for('clubct.clubContent', club_id=club_id))

    return render_template('CreateClub.html',username=username)