from flask import Flask,render_template,request,redirect,session,flash
from flask import Blueprint
from ATMflask import db
from ATMflask.sql import User

WD = Blueprint('WD',__name__)


@WD.route('/Withdrawal',methods = ['GET','POST'])
def Withdrawal():
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()
    return  render_template('Withdrawal.html',username=client.username)
