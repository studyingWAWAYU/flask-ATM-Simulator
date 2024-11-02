
import time

from flask import Blueprint
from flask import render_template, request, session, flash

from ATMflask import db
from ATMflask.sql import User

TCR = Blueprint('TCR',__name__)
timestamp = time.ctime()

@TCR.route('/Total_Card_Re',methods = ['GET','POST'])
def Total_Card_Re():
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()
    if request.method == 'GET':
        return render_template('Total_Card_Re.html',creditBalance=abs(client.creditBalance))


    pwd = request.form.get('pwd')

    if pwd == client.password:
        if client.balance >= client.creditBalance and client.creditBalance < 0:
            current_credit = abs(client.creditBalance) #临时存储
            client.balance -= current_credit  #  进行扣款
            client.creditBalance = 0   # 欠款清零

            # 获取当前时间
            timestamp = time.ctime()
            # 记录明细
            client.ICDetail += timestamp + "还款扣费%s元\n"%current_credit
            client.CreditDetail += timestamp + "还款%s元\n"%current_credit
            db.session.commit()
            flash('一键还款' + str(current_credit) + '元，您本期欠款已还清!')
            return render_template('Total_Card_Re.html',creditBalance=abs(client.creditBalance))

        elif client.balance >= client.creditBalance and client.creditBalance == 0:
            flash("您本期欠款为0，无需还款")
            return render_template('Total_Card_Re.html',creditBalance=abs(client.creditBalance))

        else:
            flash("您的IC卡余额不足！请充值后再还款！")
            return render_template('Total_Card_Re.html',creditBalance=abs(client.creditBalance))

    else:
        flash("密码错误!")
        return render_template('Total_Card_Re.html',creditBalance=abs(client.creditBalance))
