import time

from flask import render_template,request,redirect, flash,session
from flask import Blueprint

from ATMflask import db
from ATMflask.sql import User

pW = Blueprint('pW',__name__)

@pW.route('/passbookWithdrawal',methods = ['GET','POST'])#用装饰器定义路由的对应关系
def passbookWithdrawal():
    if request.method =='GET':
        return render_template('passbookWithdrawal.html')
    passbookWithdrawal_entitledNum = request.form.get('passbookWithdrawal_entitledNum')#获取POST传过来的值
    if passbookWithdrawal_entitledNum:
        try:
            amount = int(request.form.get('amount'))
            # 获取当前客户client的信息
            user_info = session.get('user_info.py')
            if user_info:
                return redirect('/login')
            id = session.get('id')
            client = db.session.query(User).filter(User.id == id).first()

            # 验证passbookWithdrawal_entitleNum是否正确
            if passbookWithdrawal_entitledNum == client.passbookWithdrawal_entitledNum:
                if client.balance > amount:
                    client.balance -= amount
                    db.session.commit()
                    # 获取时间
                    timestamp = time.ctime()
                    # client添加ICDetail
                    client.ICDetail += timestamp + "取款" + str(amount) + "元;"
                    flash('取款成功！')
                else:
                    flash('余额不足，取款失败！')

            else:
                flash('6位取款授权码输入错误！')
        except ValueError:
            pass
    else:
        flash('取款授权码不能为空！')

    return render_template('passbookWithdrawal.html')
