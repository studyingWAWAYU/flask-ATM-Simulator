from flask import Flask,render_template,request,redirect,session,flash
from flask import Blueprint
from ATMflask import db
from ATMflask.sql import User

AFD = Blueprint('AFD',__name__)

@AFD.route('/accumulationFundDetail',methods = ['GET','POST'])
def accumulationFundDetail():
    user_info = session.get('user_info.py')
    if user_info:
        return redirect('/login')
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    return  render_template('accumulationFundDetail.html',username=client.username,accumulationFundDetail=client.accumulationFundDetail)
