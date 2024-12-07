from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import ATMflask.settings as settings

app = Flask(__name__)  # 实例化flask对象
app.config.from_object(settings)  # 配置文件
db = SQLAlchemy(app)  # 实例化数据库对象，它提供访问Flask-SQLAlchemy的所有功能

from ATMflask.views import index
app.register_blueprint(index.idx)

from ATMflask.views import Authentication
app.register_blueprint(Authentication.auth)

from ATMflask.views import MyProfile
app.register_blueprint(MyProfile.myProf)

from ATMflask.views import MyActivity
app.register_blueprint(MyActivity.myAct)

from ATMflask.views import ActivityManage
app.register_blueprint(ActivityManage.actManage)

from ATMflask.views import ActivityLobby
app.register_blueprint(ActivityLobby.actlb)

from ATMflask.views import ActivityContent
app.register_blueprint(ActivityContent.actct)

from ATMflask.views import ClubLobby
app.register_blueprint(ClubLobby.clublb)

from ATMflask.views import ClubContent
app.register_blueprint(ClubContent.clubct)

from ATMflask.views import MyClub
app.register_blueprint(MyClub.myclub)

from ATMflask.views import ParticipantsManage
app.register_blueprint(ParticipantsManage.parManage)