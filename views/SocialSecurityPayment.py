
import time

from flask import Blueprint
from flask import render_template, request, session, flash

from ATMflask import db
from ATMflask.sql import User

SSP = Blueprint('SSP',__name__)
timestamp = time.ctime()

@SSP.route('/SocialSecurityPayment',methods = ['GET','POST'])
def SocialSecurityPayment():
    if request.method == 'GET':
        return render_template('SocialSecurityPayment.html')
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    pwd = request.form.get('pwd') # 获取POST传过来的值
    number = request.form.get('number')

    if pwd == client.password:
        if client.balance >= int(number):
            client.balance -= int(number)  # 进行缴费扣费
            # 获取当前时间
            timestamp = time.ctime()
            # 记录明细
            client.ICDetail += timestamp + "社保缴费支出"+number+"元\n"
            db.session.commit()
            flash("社保缴费成功!")
            return render_template('SocialSecurityPayment.html')
        else:
            flash("您的IC卡余额不足！请充值后再缴费！")
            return render_template('SocialSecurityPayment.html')
    else:
        flash("密码错误!")
        return render_template('SocialSecurityPayment.html')