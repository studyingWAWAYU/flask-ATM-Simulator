from flask_migrate import Migrate
from sqlalchemy import ForeignKey

import ATMflask.settings as settings
from ATMflask import app,db


#配置数据库
HOSTNAME = "127.0.0.1"
PORT = "3306"
USERNAME = 'root'
PASSWORD = 'root'
DATABASE = 'acthub'

#mysql+pymysql://数据库用户名:密码@127.0.0.1:3306/数据库名
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
#设置后，在每次请求结束后会自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = settings.SQLALCHEMY_COMMIT_ON_TEARDOWN
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_POOL_RECYCLE'] = settings.SQLALCHEMY_POOL_RECYCLE


migrate = Migrate(app,db)

#db.metadata.clear()  #改模型之前要先把原来的删掉

#ORM对象关系映射
class User(db.Model):
    #定义表名
    __tablename__ = "User"
    #ID设为主键
    id = db.Column(db.Integer,primary_key=True,unique=True,autoincrement=True)
    username = db.Column(db.String(20),unique = True,nullable=False)
    password = db.Column(db.String(15),nullable=False)
    gender = db.Column(db.Enum("Male","Female","Non-binary"),nullable=True)
    phoneNumber = db.Column(db.String(15),nullable=False)
    MyClubId = db.Column(db.String(200),nullable=True)
    MyActivityId = db.Column(db.String(200),nullable=True)

class Membership(db.Model):
    __tablename__ = "Membership"
    club_id = db.Column(db.Integer,ForeignKey("Club.club_id"),primary_key=True)
    user_id = db.Column(db.Integer,ForeignKey("User.id"),primary_key=True)
    role = db.Column(db.Enum("member","manager"),nullable=False)
    join_time = db.Column(db.Date,nullable=True)

class Club(db.Model):
    __tablename__ = "Club"
    club_id = db.Column(db.Integer,primary_key=True,unique=True,autoincrement=True)
    club_name = db.Column(db.String(50),nullable=False,unique=True)
    description = db.Column(db.String(1000),nullable=True)
    created_time = db.Column(db.Date,nullable=False)

class Participant(db.Model):
    __tablename__ = "Participant"
    activity_id = db.Column(db.Integer,ForeignKey("Activity.activity_id"),primary_key=True)
    user_id = db.Column(db.Integer,ForeignKey("User.id"),primary_key=True)
    status = db.Column(db.Enum("Registered","Confirmed","Absent","Present"),nullable=False)
    role = db.Column(db.String(50),nullable=True)

class Activity(db.Model):
    __tablename__ = "Activity"
    activity_id = db.Column(db.Integer,primary_key=True,unique=True,autoincrement=True)
    activity_name = db.Column(db.String(50),nullable=False)
    description = db.Column(db.String(1000),nullable=True)
    type = db.Column(db.Enum("Cultural Events","Social Events","Career Development","Study Trips",
                             "Academic Activities","Interest Groups","Sports","Volunteer Work"),nullable=False)
    status = db.Column(db.Enum("Upcoming","Ongoing","Completed"),nullable=False)
    contact_id = db.Column(db.Integer,nullable=True)
    location = db.Column(db.String(80),nullable=False)
    club_id = db.Column(db.Integer,nullable=False)
    start_time = db.Column(db.DateTime,nullable=False)
    end_time = db.Column(db.DateTime,nullable=False)
    signin_code = db.Column(db.String(6),nullable=True)
    signup_start = db.Column(db.DateTime,nullable=False)
    signup_end = db.Column(db.DateTime,nullable=False)
    max_participant = db.Column(db.Integer,nullable=False)


'''
with app.test_request_context():
    db.create_all() #建表，建过之后注释掉
    #db.drop_all() #删除表，如果要重新建表


#写入数据，写过之后注释掉
with app.test_request_context():
    #创建ORM对象
    user1 = User(username ="Arial", password="12345678", gender="Female", phoneNumber="12340354635256")

    #将ORM对象添加到db.session中
    db.session.add_all([user1])

    #将db.session中的改变同步到数据库
'''