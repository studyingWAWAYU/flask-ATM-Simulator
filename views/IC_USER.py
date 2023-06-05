
from flask import Flask,render_template,request,redirect,session,flash
from flask import Blueprint
from ATMflask import db
from ATMflask.sql import User
import time

ICU = Blueprint('ICU',__name__)

@ICU.route('/IC_USER',methods = ['GET','POST'])
def IC_USER():
    if request.method == 'GET':
        return render_template('IC_USER.html')
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    pwd = request.form.get('pwd')# 获取POST传过来的值
    number = request.form.get('number')
    user1 = request.form.get('id')
    client1 = db.session.query(User).filter(User.id == user1).first()
    print(user1+"111")

    if client1 != None:
        if pwd == client1.password:
            client1.balance += int(number)  # 进行充值
            # 获取当前时间
            timestamp = time.ctime()
            # 记录明细
            client1.ICDetail += timestamp + "成功充值" + number + "元\n"
            db.session.commit()
            flash("充值成功!")
            return render_template('IC_USER.html')
        else:
            flash("密码或id错误!")
            return render_template('IC_USER.html')
    else:
        flash("请输入正确id")
        return render_template('IC_USER.html')