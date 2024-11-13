from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import ATMflask.settings as settings


app = Flask(__name__)#实例化flask对象
app.config.from_object(settings)#配置文件
db = SQLAlchemy(app)#实例化数据库对象，它提供访问Flask-SQLAlchemy的所有功能


from ATMflask.views import index
app.register_blueprint(index.idx)

from ATMflask.views import loginANDregister
app.register_blueprint(loginANDregister.lr)

from ATMflask.views import ModifyPassword
app.register_blueprint(ModifyPassword.MP)

from ATMflask.views import ActivityLobby
app.register_blueprint(ActivityLobby.actlb)





