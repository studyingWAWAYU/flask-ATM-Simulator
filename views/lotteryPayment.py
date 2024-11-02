
import time

from flask import Blueprint
from flask import render_template, request, session, flash

from ATMflask import db
from ATMflask.sql import User

LP = Blueprint('LP',__name__)
timestamp = time.ctime()

@LP.route('/lotteryPayment',methods = ['GET','POST'])
def lotteryPayment():
    if request.method == 'GET':
        return render_template('lotteryPayment.html')
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    pwd = request.form.get('pwd') # 获取POST传过来的值
    number = request.form.get('number')

    if pwd==client.password:
        if client.balance >= int(number):
            client.balance -= int(number) # 进行缴费扣费
            # 获取当前时间
            timestamp = time.ctime()
            #记录明细
            client.ICDetail+=timestamp+"体彩缴费%s元\n"%int(number)
            db.session.commit()
            flash("缴费成功!")
            return render_template('lotteryPayment.html')
        else:
            flash("您的IC卡余额不足！请充值后再缴费！")
            return render_template('lotteryPayment.html')
    else:
        flash("密码错误!")
        return render_template('lotteryPayment.html')
