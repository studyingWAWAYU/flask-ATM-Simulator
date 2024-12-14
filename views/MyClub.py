from flask import render_template,request,redirect,flash,session
from flask import Blueprint

from ATMflask import db,app
from ATMflask.sql import User,Club,Membership

from flask_sqlalchemy import SQLAlchemy

myclub = Blueprint('myclub', __name__)

'''
实现功能：
    1. 创建社团
    2. 编辑社团信息
    3. 删除社团
'''

# 显示所有社团
@myclub.route('/MyClub', methods=['POST', 'GET'])
def MyClub():
    # ----------------- 当前登录用户部分 -------------------#
    user_id = session.get('id')
    username = None
    club_details = []
    search_query = request.args.get('search', '').strip()  # 获取搜索框的内容

    if user_id:
        user = User.query.get(user_id)
        username = user.username

        # 获取当前用户参与的社团，包括社团、用户角色
        user_clubs = db.session.query(Club, Membership.role).join(Membership).filter(
            Membership.user_id == user_id).all()

        # 获取每个社团的 manager 和成员人数
        for club, role in user_clubs:
            # 获取社团的经理（role="manager"）
            manager = db.session.query(User.username).join(Membership).filter(
                Membership.club_id == club.club_id, Membership.role == 'manager'
            ).first()

            # 获取社团的成员人数
            member_count = db.session.query(Membership).filter(
                Membership.club_id == club.club_id
            ).count()

            # 将社团、经理和成员人数打包成一个元组，存储到 club_details 中
            club_details.append((club, manager.username if manager else None, member_count))

        # ---------------- 搜索查询功能 -------------------#
        if search_query:
            # 根据用户输入的关键字过滤当前用户的社团
            club_details = [
                (club, manager, num_members)
                for club, manager, num_members in club_details
                if search_query.lower() in club.club_name.lower()
            ]

    return render_template(
        'MyClub.html',
        user_clubs=club_details,
        user_id=user_id,
        username=username,
        search_query=search_query,
        search_message="No clubs match your search." if search_query and not club_details else None
    )

