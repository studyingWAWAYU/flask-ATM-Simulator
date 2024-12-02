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
@myclub.route('/MyClub', methods=['post', 'get'])
def MyClub():

    # ----------------- 当前登录用户部分 -------------------#
    user_id = session.get('id')
    username = None
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

        # ---------------- 搜索查询功能 -------------------#



    return render_template('MyClub.html', user_clubs=club_details, user_id=user_id,username=username)


'''
# 创建社团
@clublb.route('/CreateClub', methods=['GET', 'POST'])
def create_club():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        new_club = Club(name=name, description=description)
        db.session.add(new_club)
        db.session.commit()
        flash('Club created successfully!')
        return redirect(url_for(''))

    return render_template('ClubLobby.html')


# 编辑社团
@clublb.route('/edit_club/<int:club_id>', methods=['GET', 'POST'])
def edit_club(club_id):
    club = Club.query.get_or_404(club_id)
    if request.method == 'POST':
        club.name = request.form.get('name')
        club.description = request.form.get('description')
        db.session.commit()
        flash('Club updated successfully!')
        return redirect(url_for('clublb.clublb'))

    return render_template('edit_club.html', club=club)


# 删除社团
@clublb.route('/delete_club/<int:club_id>', methods=['POST'])
def delete_club(club_id):
    club = Club.query.get_or_404(club_id)
    db.session.delete(club)
    db.session.commit()
    flash('Club deleted successfully!')
    return redirect(url_for('clublb.html'))
'''
