from flask import Flask,render_template,request,redirect,session,flash
from flask import Blueprint
from ATMflask import db
from ATMflask.sql import User

AFS = Blueprint('AFS',__name__)


@AFS.route('/accumulationFundService',methods = ['GET','POST'])
def accumulationFundService():
    user_info = session.get('user_info.py')
    if user_info:
        return redirect('/login')
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    return  render_template('accumulationFundService.html',username=client.username,accumulationFund=client.accumulationFund)
