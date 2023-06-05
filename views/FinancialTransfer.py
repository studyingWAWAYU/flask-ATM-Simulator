from flask import render_template,request,redirect, flash,session
from flask import Blueprint

from ATMflask import db
from ATMflask.sql import User

import time

FT = Blueprint('FT',__name__)

@FT.route('/FinancialTransfer',methods = ['GET','POST'])#用装饰器定义路由的对应关系
def FinancialTransfer():
    if request.method == 'GET':
        return render_template('FinancialTransfer.html')

    receiver_id = request.form.get('receiver_id')  # 获取POST传过来的值
    if receiver_id:
        pwd = request.form.get('pwd')
        if pwd:
            try:
                amount = int(request.form.get('amount'))
                # 获取当前客户client的信息
                user_info = session.get('user_info.py')
                if user_info:
                    return redirect('/login')
                id = session.get('id')
                client = db.session.query(User).filter(User.id == id).first()

                # 获取接受理财转账的用户receiver的信息
                receiver = db.session.query(User).filter(User.id == receiver_id).first()

                # 验证理财转账密码
                if pwd == client.password:
                    if client.financialBalance >= amount:
                        client.financialBalance -= amount
                        receiver.balance += amount
                        # 获取当前时间
                        timestamp = time.ctime()
                        # client的理财明细FinancialDetail添加
                        client.FinancialDetail += timestamp + "向用户" + receiver.username + "转账" + str(
                            amount) + "元;"
                        # receive的ICDetail添加
                        receiver.ICDetail += timestamp + "收到用户" + client.username + "的转账" + str(
                            amount) + "元;"
                        db.session.commit()
                        flash("转账成功!")
                    else:
                        flash("您的理财卡余额不足！请充值后再转账")
                else:
                    flash("密码错误!")
            except ValueError:
                pass
        else:
            flash('接款方ID号或理财卡密码不能为空！')
    else:
        flash('接款方ID号或理财卡密码不能为空！')

    return render_template('FinancialTransfer.html')





