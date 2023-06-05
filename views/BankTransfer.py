from flask import Flask,render_template,request,redirect,session,flash
from flask import Blueprint
from ATMflask import db
from ATMflask.sql import User
import time

BT = Blueprint('BT',__name__)

@BT.route('/BankTransfer',methods = ['GET','POST'])
def BankTransfer():
    if request.method == 'GET':
        return render_template('BankTransfer.html')
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    pwd = request.form.get('pwd')
    user1 = request.form.get('id')        #获取POST传过来的值
    number = request.form.get('number')   #获取POST传过来的值
    client1 = db.session.query(User).filter(User.id == user1).first()

    if pwd==client.password:
        if client.balance >= int(number):
            client.balance -= int(number) # 进行转出
            client1.balance += int(number)  # 转入另一账号
            # 获取当前时间
            timestamp = time.ctime()
            #记录明细
            client.ICDetail+=timestamp+"向用户"+client1.username+"转账"+number+"元\n"
            client1.ICDetail+=timestamp+"收到用户"+client.username+"的转账"+number+"元\n"
            db.session.commit()
            flash("转账成功!")
            return render_template('Transfer_resent.html',username=client1.username) #进行跳转
        else:
            flash("您的IC卡余额不足！请充值后再转账")
            return render_template('BankTransfer.html')
    else:
        flash("密码错误或收款方id不存在!")
        return render_template('BankTransfer.html')
