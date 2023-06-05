from flask_migrate import Migrate
import ATMflask.settings as settings
from ATMflask import app,db


#配置数据库
HOSTNAME = "127.0.0.1"
PORT = "3306"
USERNAME = 'root'
PASSWORD = 'root'
DATABASE = 'atm'

#mysql+pymysql://数据库用户名:密码@127.0.0.1:3306/数据库名
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
#设置后，在每次请求结束后会自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = settings.SQLALCHEMY_COMMIT_ON_TEARDOWN
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_POOL_RECYCLE'] = settings.SQLALCHEMY_POOL_RECYCLE


migrate = Migrate(app,db)

#ORM对象关系映射
class User(db.Model):
    #定义表名
    __tablename__ = "ATM"
    #ID设为主键
    id = db.Column(db.Integer,primary_key=True,unique=True,autoincrement=True)
    username = db.Column(db.String(10),unique = True,nullable=False)
    password = db.Column(db.String(10),nullable=False)
    balance = db.Column(db.Integer,nullable=False)
    creditBalance = db.Column(db.Integer,nullable=False)
    multiBalance = db.Column(db.String(50),nullable=False)
    accumulationFund = db.Column(db.Integer,nullable=False)
    financialBalance = db.Column(db.Integer,nullable=False)
    ICDetail = db.Column(db.String(1000),nullable=False)
    accumulationFundDetail= db.Column(db.String(1000),nullable=False)
    FinancialDetail= db.Column(db.String(1000),nullable=False)
    CreditDetail= db.Column(db.String(1000),nullable=False)
    passbookWithdrawal_entitledNum = db.Column(db.String(6),nullable=False)

'''
with app.test_request_context():
    db.create_all()#建表，建过之后注释掉
    #db.drop_all()#删除表，如果要重新建表


#写入数据，写过之后注释掉
with app.test_request_context():
    #创建ORM对象
    user1 = User(username ="刘一", password="123", balance=500, creditBalance=-100,multiBalance="人民币:500  美元:200  欧元:0", accumulationFund=200,financialBalance=1000,ICDetail="Sat May 27 21:04:29 2023 IC卡存款500元\n",accumulationFundDetail="",FinancialDetail="Sat May 27 21:04:29 2023 理财卡存款1000元\n",CreditDetail="",passbookWithdrawal_entitledNum="123456")
    user2 = User(username ='陈二', password='132', balance=500, creditBalance=-100,multiBalance="人民币:500  美元:200  欧元:0", accumulationFund=200,financialBalance=1000,ICDetail="Sat May 27 21:04:29 2023 IC卡存款500元\n",accumulationFundDetail="",FinancialDetail="Sat May 27 21:04:29 2023 理财卡存款1000元\n",CreditDetail="",passbookWithdrawal_entitledNum="234561")
    user3 = User(username ='张三', password='213', balance=500, creditBalance=-100,multiBalance="人民币:500  美元:200  欧元:0", accumulationFund=200,financialBalance=1000,ICDetail="Sat May 27 21:04:29 2023 IC卡存款500元\n",accumulationFundDetail="",FinancialDetail="Sat May 27 21:04:29 2023 理财卡存款1000元\n",CreditDetail="",passbookWithdrawal_entitledNum="345612")
    user4 = User(username = '李四',password='231', balance=500, creditBalance=-100,multiBalance="人民币:500  美元:200  欧元:0", accumulationFund=200,financialBalance=1000,ICDetail="Sat May 27 21:04:29 2023 IC卡存款500元\n",accumulationFundDetail="",FinancialDetail="Sat May 27 21:04:29 2023 理财卡存款1000元\n",CreditDetail="",passbookWithdrawal_entitledNum="456123")
    user5 = User(username = '王五',password='321', balance=500, creditBalance=-100,multiBalance="人民币:500  美元:200  欧元:0", accumulationFund=200,financialBalance=1000,ICDetail="Sat May 27 21:04:29 2023 IC卡存款500元\n",accumulationFundDetail="",FinancialDetail="Sat May 27 21:04:29 2023 理财卡存款1000元\n",CreditDetail="",passbookWithdrawal_entitledNum="561234")
    user6 = User(username = '赵六',password='312', balance=500, creditBalance=-100,multiBalance="人民币:500  美元:200  欧元:0", accumulationFund=200,financialBalance=1000,ICDetail="Sat May 27 21:04:29 2023 IC卡存款500元\n",accumulationFundDetail="",FinancialDetail="Sat May 27 21:04:29 2023 理财卡存款1000元\n",CreditDetail="",passbookWithdrawal_entitledNum="213456")
    user7 = User(username = '孙七',password='112', balance=500, creditBalance=-100,multiBalance="人民币:500  美元:200  欧元:0", accumulationFund=200,financialBalance=1000,ICDetail="Sat May 27 21:04:29 2023 IC卡存款500元\n",accumulationFundDetail="",FinancialDetail="Sat May 27 21:04:29 2023 理财卡存款1000元\n",CreditDetail="",passbookWithdrawal_entitledNum="312456")
    user8 = User(username = '周八',password='113', balance=500, creditBalance=-100,multiBalance="人民币:500  美元:200  欧元:0", accumulationFund=200,financialBalance=1000,ICDetail="Sat May 27 21:04:29 2023 IC卡存款500元\n",accumulationFundDetail="",FinancialDetail="Sat May 27 21:04:29 2023 理财卡存款1000元\n",CreditDetail="",passbookWithdrawal_entitledNum="712345")
    user9 = User(username = '吴九',password='223', balance=500, creditBalance=-100,multiBalance="人民币:500  美元:200  欧元:0", accumulationFund=200,financialBalance=1000,ICDetail="Sat May 27 21:04:29 2023 IC卡存款500元\n",accumulationFundDetail="",FinancialDetail="Sat May 27 21:04:29 2023 理财卡存款1000元\n",CreditDetail="",passbookWithdrawal_entitledNum="923456")
    user10 = User(username ='郑十',password='333', balance=500, creditBalance=-100,multiBalance="人民币:500  美元:200  欧元:0", accumulationFund=200,financialBalance=1000,ICDetail="Sat May 27 21:04:29 2023 IC卡存款500元\n",accumulationFundDetail="",FinancialDetail="Sat May 27 21:04:29 2023 理财卡存款1000元\n",CreditDetail="",passbookWithdrawal_entitledNum="523456")

    #将ORM对象添加到db.session中
    db.session.add_all([user1,user2,user3,user4,user5,user6,user7,user8,user9,user10])

    #将db.session中的改变同步到数据库'''
