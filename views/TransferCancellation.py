
from flask import Flask,render_template,request,redirect,session,flash
from flask import Blueprint
from ATMflask import db
from ATMflask.sql import User
import time

TC = Blueprint('TC',__name__)


@TC.route('/TransferCancellation',methods = ['GET','POST'])
def TransferCancellation():
    if request.method == 'GET':
        return render_template('TransferCancellation.html')
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    pwd = request.form.get('pwd')
    user1 = request.form.get('id')  # 获取POST传过来的值
    number = request.form.get('number')

    client1 = db.session.query(User).filter(User.id == user1).first()

    resent = client.ICDetail.split(";")
    for i in range(len(resent)):        # 遍历每一次的明细
        resent_name_word = resent[i]    # 读取列表中的每一个元素
        if client1.username in resent_name_word and pwd == client.password and number in resent_name_word:   # 防止转账信息错误
            if client1.balance >= int(number):
               client1.balance -= int(number)  # 进行撤销
               client.balance += int(number)  # 转入自己账号
               # 获取当前时间
               timestamp = time.ctime()
               # 记录明细
               client.ICDetail += timestamp + "向用户" + client1.username + "撤销转账" + number + "元\n"
               client1.ICDetail += timestamp + "用户" + client.username + "撤销转账" + number + "元\n"
               db.session.commit()
               flash("撤销转账成功!")
               return render_template('TransferCancellation.html')
            else:
                client.balance += int(number)  # 转入自己账号
                client1.creditBalance -= int(number)  # 进行扣费
                # 获取当前时间
                timestamp = time.ctime()
                # 记录明细
                client.ICDetail += timestamp + "向用户" + client1.username + "撤销转账" + number + "元\n"
                client1.CreditDetail += timestamp + "用户" + client.username + "撤销转账" + number + "元,您余额不足，已欠款\n"
                db.session.commit()
                flash("撤销转账成功!")
                return render_template('TransferCancellation.html')

    flash("密码错误或撤销转款方id错误或金额错误!")
    return render_template('TransferCancellation.html')
