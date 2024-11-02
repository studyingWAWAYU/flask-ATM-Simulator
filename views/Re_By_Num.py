import time

from flask import Blueprint
from flask import render_template, request, session, flash

from ATMflask import db
from ATMflask.sql import User

RBN = Blueprint('RBN',__name__)
timestamp = time.ctime()

@RBN.route('/Re_By_Num',methods = ['GET','POST'])
def Re_By_Num():
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()
    if request.method == 'GET':
        return render_template('Re_By_Num.html',creditBalance=abs(client.creditBalance))



    pwd = request.form.get('pwd')
    user1 = request.form.get('id')  # 获取POST传过来的值
    client1 = db.session.query(User).filter(User.id == user1).first()

    if pwd == client.password:
        if client.balance >= client1.creditBalance and client1.creditBalance < 0:
            current_num = abs(client1.creditBalance)  # 临时存储
            client.balance -= current_num
            client1.creditBalance = 0
            # 获取当前时间
            timestamp = time.ctime()
            # 记录明细
            client.ICDetail += timestamp + "还款扣除%s元;"%current_num
            client1.CreditDetail += timestamp + "收到用户" + client.username + "的代还款%s元\n"%current_num
            db.session.commit()
            flash('还款' + str(current_num) + '元，您的欠款已还清!')
            return render_template('Re_By_Num.html',creditBalance=abs(client.creditBalance))
        elif client.balance >= client1.creditBalance and client1.creditBalance == 0:
            flash("该id的欠款已还清！")
            return render_template('Re_By_Num.html',creditBalance=abs(client.creditBalance))
        else:
            flash("您的IC卡余额不足！请充值后再还账")
            return render_template('Re_By_Num.html',creditBalance=abs(client.creditBalance))

    else:
        flash("密码错误或代还款方id不存在!")
        return render_template('Re_By_Num.html')
