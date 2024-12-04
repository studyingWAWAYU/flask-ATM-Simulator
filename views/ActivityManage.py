import os.path
from flask import render_template,request,redirect, flash,session
from flask import Blueprint
from datetime import datetime, timedelta

from ATMflask import db
from ATMflask.sql import User,Activity,Club,Participant,Membership
import shutil

actManage = Blueprint('actManage',__name__)

@actManage.route('/AddActivity',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def addActivity():
    # 判断用户是否登录
    user_id = session.get('id')
    username = None
    myClubNameLST = None
    myClubIdLST = None
    current_time = datetime.now()
    nowTime = current_time.strftime('%Y-%m-%dT%H:%M')
    # 加一天
    newTime_dt = current_time + timedelta(days=1)
    newTime = newTime_dt.strftime('%Y-%m-%dT%H:%M')

    if user_id:
        user = User.query.get(user_id)
        username = user.username

        # 查询用户作为manager的所有社团，结果是列表嵌套元组，例如[(1,),(2,)]
        myClubId = db.session.query(Membership.club_id).filter_by(user_id=user_id,role='manager').all()
        myClubIdLST = [club_id[0] for club_id in myClubId]  # 把列表嵌套元组改为列表
        myClubName = db.session.query(Club.club_name).filter(Club.club_id.in_(myClubIdLST)).all()
        myClubNameLST = [club_name[0] for club_name in myClubName]

    if request.method == 'GET':
        return render_template('AddActivity.html',username=username,myClubNameLST=myClubNameLST,nowTime=nowTime,newTime=newTime)


    if request.method == 'POST':
        # 从表单取数据
        actTitle = request.form.get('ActTitle')
        club = request.form.get('clubs')
        type = request.form.get('types')
        location = request.form.get('location')
        max_participant = request.form.get('max_participant')
        actStart = request.form.get('actStart')
        actEnd = request.form.get('actEnd')
        contact = request.form.get('contact')
        enrollStart = request.form.get('enrollStart')
        enrollEnd = request.form.get('enrollEnd')
        roles = request.form.get('roles')
        requirement = request.form.get('requirement')
        description = request.form.get('description')

        # 判断不可为NULL的值
        if actTitle=="":
            flash("Activity Title cannot be empty.")
            return render_template('AddActivity.html', username=username, myClubNameLST=myClubNameLST,nowTime=nowTime,newTime=newTime)
        elif location == "":
            flash("Location cannot be empty.")
            return render_template('AddActivity.html', username=username, myClubNameLST=myClubNameLST,nowTime=nowTime,newTime=newTime)
        elif max_participant is None:
            flash("Maximum Participant cannot be empty")
            return render_template('AddActivity.html', username=username, myClubNameLST=myClubNameLST,nowTime=nowTime,newTime=newTime)

        # 与当前时间对比得到活动status, 将字符串转为 datetime 对象
        actStart = datetime.strptime(actStart, "%Y-%m-%dT%H:%M")
        actEnd = datetime.strptime(actEnd, "%Y-%m-%dT%H:%M")
        enrollStart = datetime.strptime(enrollStart, "%Y-%m-%dT%H:%M")
        enrollEnd = datetime.strptime(enrollEnd, "%Y-%m-%dT%H:%M")
        # 确定活动状态
        if current_time < actStart:
            status = 'upcoming'
        elif actStart <= current_time <= actEnd:
            status = 'ongoing'
        else:
            status = 'completed'

        # 从club_name拿到club_id
        club_id_selected = myClubIdLST[myClubNameLST.index(club)]
        # 将数据放进数据库
        newAct = Activity(activity_name=actTitle, type=type, status=status, contact=contact, location=location,
                          club_id=club_id_selected, start_time=actStart, end_time=actEnd,
                          signup_start=enrollStart,
                          signup_end=enrollEnd, roles=roles, requirement=requirement, description=description,
                          max_participant=max_participant)
        db.session.add(newAct)
        db.session.commit()

        participant_manager = Participant(activity_id=newAct.activity_id, user_id=user_id, status='Registered',
                                          role='manager')
        db.session.add(participant_manager)
        db.session.commit()

        # 上传图片
        # 定义允许的图片格式
        ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
        def allowed_file(filename):
            # 获取文件的扩展名
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        if 'photo[]' in request.files:
            files = request.files.getlist('photo[]')
            if len(files) > 8:
                flash("You can only upload up to 8 images.")
                return render_template('AddActivity.html', username=username, myClubNameLST=myClubNameLST,
                                       nowTime=nowTime, newTime=newTime)
            for file in files:
                if file and allowed_file(file.filename):
                    activity_id = db.session.query(Activity.activity_id).filter_by(activity_name=actTitle).first()
                    if activity_id:
                        # 配置上传文件目录
                        #提取新activity的id，保存图片的路径为os.getcwd()+static/img/uploads/activity/ + activity_id + filename
                        upload_dir = os.path.join(os.getcwd(),'static','img','uploads',str(activity_id[0]))
                        if not os.path.exists(upload_dir):
                            os.makedirs(upload_dir)
                        file.save(os.path.join(upload_dir,file.filename))
                        flash("Images uploaded successfully.")

                else:
                    flash("Illegal image format: Please upload images in JPG, JPEG, PNG or GIF format!")
                    return render_template('AddActivity.html', username=username, myClubNameLST=myClubNameLST,
                                           nowTime=nowTime, newTime=newTime)

        #return render_template('AddActivity.html',username=username,myClubNameLST=myClubNameLST)
        return redirect('/MyActivity')




@actManage.route('/EditActivity/<int:activity_id>',methods=['GET','POST'])
def EditActivity(activity_id):
    user_id = session.get('id')
    username = None
    actOrigin = None
    current_clubName = None

    if user_id:
        user = User.query.get(user_id)
        username = user.username
        actOrigin = Activity.query.get(activity_id)

        ClubId = actOrigin.club_id
        current_clubName = db.session.query(Club.club_name).filter_by(club_id=ClubId).scalar()


    # 查询用户作为manager的所有社团，结果是列表嵌套元组，例如[(1,),(2,)]
    myClubId = db.session.query(Membership.club_id).filter_by(user_id=user_id, role='manager').all()
    myClubIdLST = [club_id[0] for club_id in myClubId]  # 把列表嵌套元组改为列表
    myClubName = db.session.query(Club.club_name).filter(Club.club_id.in_(myClubIdLST)).all()
    myClubNameLST = [club_name[0] for club_name in myClubName]

    actTypes = ["Cultural Events","Social Events","Career Development","Study Trips",
                "Academic Activities","Interest Groups","Sports","Volunteer Work"]

    if request.method == 'GET':
        return render_template('EditActivity.html',username=username,actOrigin=actOrigin,current_clubName=current_clubName,
                               myClubNameLST=myClubNameLST,actTypes=actTypes)

    if request.method == 'POST':
        # 从表单取数据
        actTitle = request.form.get('ActTitle')
        club = request.form.get('clubs')
        type = request.form.get('types')
        location = request.form.get('location')
        max_participant = request.form.get('max_participant')
        actStart = request.form.get('actStart')
        actEnd = request.form.get('actEnd')
        contact = request.form.get('contact')
        enrollStart = request.form.get('enrollStart')
        enrollEnd = request.form.get('enrollEnd')
        roles = request.form.get('roles')
        requirement = request.form.get('requirement')
        description = request.form.get('description')

        # 判断不可为NULL的值
        if actTitle == "":
            flash("Activity Title cannot be empty.")
            return render_template('EditActivity.html', username=username, actOrigin=actOrigin,
                                   current_clubName=current_clubName,
                                   myClubNameLST=myClubNameLST, actTypes=actTypes)
        elif location == "":
            flash("Location cannot be empty.")
            return render_template('EditActivity.html', username=username, actOrigin=actOrigin,
                                   current_clubName=current_clubName,
                                   myClubNameLST=myClubNameLST, actTypes=actTypes)
        elif max_participant is None:
            flash("Maximum Participant cannot be empty")
            return render_template('EditActivity.html', username=username, actOrigin=actOrigin,
                                   current_clubName=current_clubName,
                                   myClubNameLST=myClubNameLST, actTypes=actTypes)

        # 检查新actTitle是否已存在
        if actTitle != actOrigin.activity_name:
            existing_actname = Activity.query.filter_by(activity_name = actTitle).one_or_none()
            if existing_actname:
                flash('Activity title already taken.')
                return render_template('EditActivity.html', username=username, actOrigin=actOrigin,
                                       current_clubName=current_clubName,
                                       myClubNameLST=myClubNameLST, actTypes=actTypes)
            else:
                Activity.activity_name = actTitle

        # 与当前时间对比得到活动status
        current_time = datetime.now()
        # 将字符串转为 datetime 对象
        actStart = datetime.strptime(actStart, "%Y-%m-%dT%H:%M")
        actEnd = datetime.strptime(actEnd, "%Y-%m-%dT%H:%M")
        enrollStart = datetime.strptime(enrollStart, "%Y-%m-%dT%H:%M")
        enrollEnd = datetime.strptime(enrollEnd, "%Y-%m-%dT%H:%M")
        # 确定活动状态
        if current_time < actStart:
            status = 'upcoming'
        elif actStart <= current_time <= actEnd:
            status = 'ongoing'
        else:
            status = 'completed'

        # 从club_name拿到club_id
        club_id_selected = myClubIdLST[myClubNameLST.index(club)]

        # 将数据放进数据库
        actOrigin.type = type
        actOrigin.status = status
        actOrigin.contact = contact
        actOrigin.location = location
        actOrigin.club_id = club_id_selected
        actOrigin.start_time = actStart
        actOrigin.end_time = actEnd
        actOrigin.signup_start = enrollStart
        actOrigin.signup_end = enrollEnd
        actOrigin.roles = roles
        actOrigin.requirement = requirement
        actOrigin.description = description
        actOrigin.max_participant = max_participant

        db.session.commit()

        # 上传图片
        # 定义允许的图片格式
        ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

        def allowed_file(filename):
            # 获取文件的扩展名
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        file = request.files['photo']
        if file:
            if allowed_file(file.filename):
                activity_id = db.session.query(Activity.activity_id).filter_by(activity_name=actTitle).first()
                if activity_id:
                    # 配置上传文件目录
                    # 提取新activity的id，保存图片的路径为os.getcwd()+static/img/uploads/activity/ + activity_id + filename
                    upload_dir = os.path.join(os.getcwd(), 'static', 'img', 'uploads', str(activity_id[0]))
                    if not os.path.exists(upload_dir):
                        os.makedirs(upload_dir)
                    file.save(os.path.join(upload_dir, file.filename))
                    flash("Image uploaded successfully.")
                    return redirect('/ActivityContent/' + str(activity_id[0]))
            else:
                flash("Illegal image format: Please upload images in JPG, JPEG, PNG or GIF format!")

        return redirect('/ActivityContent/'+str(activity_id))

# 如果是manager就可以编辑、删除这个活动。
@actManage.route('/delete_activity/<int:activity_id>',methods=['POST'])
def delete_activity(activity_id):
    current_activity = Activity.query.get(activity_id)
    # 删除所有图片
    upload_dir = os.path.join(os.getcwd(),'static','img','uploads',str(activity_id))
    if  os.path.exists(upload_dir):
        shutil.rmtree(upload_dir)

    # 删除数据库内容
    current_participants = Participant.query.filter_by(activity_id=activity_id).all()
    for each_participant in current_participants:
        db.session.delete(each_participant)
    db.session.commit()  # 因为完整性约束，要先把Participant表中的删掉才能删Activity
    db.session.delete(current_activity)
    db.session.commit()

    return redirect("/MyActivity")