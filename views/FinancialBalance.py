from flask import Blueprint
from flask import render_template, redirect, session

from ATMflask import db
from ATMflask.sql import User

FB = Blueprint('FB',__name__)


# 理财余额查询
@FB.route('/FinancialBalance',methods = ['GET','POST'])
def FinancialBalance():
    user_info = session.get('user_info.py')
    if user_info:
        return redirect('/login')
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    return  render_template('FinancialBalance.html',username=client.username,financialBalance=client.financialBalance)
