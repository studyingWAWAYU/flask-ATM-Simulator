from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import ATMflask.settings as settings


app = Flask(__name__)#实例化flask对象
app.config.from_object(settings)#配置文件
db = SQLAlchemy(app)#实例化数据库对象，它提供访问Flask-SQLAlchemy的所有功能

# xyq
from ATMflask.views import index
app.register_blueprint(index.idx)

from ATMflask.views import loginANDregister
app.register_blueprint(loginANDregister.lr)

from ATMflask.views import InquiryService
app.register_blueprint(InquiryService.IS)

from ATMflask.views import menu
app.register_blueprint(menu.mn)

from ATMflask.views import accumulationFundService
app.register_blueprint(accumulationFundService.AFS)

from ATMflask.views import accumulationFundDetail
app.register_blueprint(accumulationFundDetail.AFD)

from ATMflask.views import multiBalance
app.register_blueprint(multiBalance.MB)

from ATMflask.views import Inquiry
app.register_blueprint(Inquiry.IQ)

from ATMflask.views import ModifyPassword
app.register_blueprint(ModifyPassword.MP)

from ATMflask.views import FinancialDetail
app.register_blueprint(FinancialDetail.FD)

from ATMflask.views import CreditDetail
app.register_blueprint(CreditDetail.CD)

# wjx
from ATMflask.views import FinancialManagement
app.register_blueprint(FinancialManagement.FM)

from ATMflask.views import FinancialBalance
app.register_blueprint(FinancialBalance.FB)

from ATMflask.views import FinancialTransfer
app.register_blueprint(FinancialTransfer.FT)


from ATMflask.views import Withdrawal
app.register_blueprint(Withdrawal.WD)

from ATMflask.views import specialWithdrawal
app.register_blueprint(specialWithdrawal.sW)

from ATMflask.views import passbookWithdrawal
app.register_blueprint(passbookWithdrawal.pW)

# zyl
from ATMflask.views import TransferAccounts
app.register_blueprint(TransferAccounts.TA)

from ATMflask.views import BankTransfer
app.register_blueprint(BankTransfer.BT)

from ATMflask.views import Transfer_resent#近期收款人
app.register_blueprint(Transfer_resent.TR)

from  ATMflask.views import CreditCardRepayment
app.register_blueprint(CreditCardRepayment.CCR)

from ATMflask.views import Recharge
app.register_blueprint(Recharge.REC)

from ATMflask.views import Total_Card_Re
app.register_blueprint(Total_Card_Re.TCR)

from ATMflask.views import Re_By_Num
app.register_blueprint(Re_By_Num.RBN)

from ATMflask.views import TransferCancellation
app.register_blueprint(TransferCancellation.TC)

from ATMflask.views import SocialSecurityPayment
app.register_blueprint(SocialSecurityPayment.SSP)

from ATMflask.views import ICPayment
app.register_blueprint(ICPayment.ICP)

from ATMflask.views import IC_USER
app.register_blueprint(IC_USER.ICU)

from ATMflask.views import lotteryPayment
app.register_blueprint(lotteryPayment.LP)