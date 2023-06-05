from flask import Flask,render_template,request,redirect,session,flash
from flask import Blueprint
from ATMflask import db
from ATMflask.sql import User

CD = Blueprint('CD',__name__)

@CD.route('/CreditDetail',methods = ['GET','POST'])
def CreditDetail():
    user_info = session.get('user_info.py')
    if user_info:
        return redirect('/login')
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    return  render_template('CreditDetail.html',username=client.username,CreditDetail=client.CreditDetail)
