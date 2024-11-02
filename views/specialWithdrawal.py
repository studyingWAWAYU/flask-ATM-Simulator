import time

from flask import render_template,request,redirect, flash,session
from flask import Blueprint

from ATMflask import db
from ATMflask.sql import User

sW = Blueprint('sW',__name__)

@sW.route('/specialWithdrawal',methods = ['GET','POST'])#用装饰器定义路由的对应关系
def specialWithdrawal():
    if request.method =='GET':
        return render_template('specialWithdrawal.html')
    specialWithdrawal_id = request.form.get('specialWithdrawal_id')#获取POST传过来的值
    if specialWithdrawal_id:
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

                # 测试specialWithdrawal和password是否正确
                if int(specialWithdrawal_id) == client.id and client.password == pwd:
                    if client.balance >= amount:
                        client.balance -= amount
                        # 获取时间
                        timestamp = time.ctime()
                        # client添加ICDetail
                        client.ICDetail += timestamp + "取款" + str(amount) + "元;"
                        db.session.commit()
                        flash('取款成功！')
                        return render_template('specialWithdrawal.html')
                    else:
                        flash('余额不足，取款失败！')
                        return render_template('specialWithdrawal.html')

                else:
                    flash('ID输入错误或密码不正确！')
            except ValueError:
                pass
        else:
            flash("ID号或特约取款密码不能为空！")
    else:
        flash('ID号或特约取款密码不能为空！')

    return render_template('specialWithdrawal.html')

