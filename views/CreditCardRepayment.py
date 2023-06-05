from flask import Flask,render_template,request,redirect,session,flash
from flask import Blueprint
from ATMflask import db
from ATMflask.sql import User

CCR = Blueprint('CCR',__name__)


@CCR.route('/CreditCardRepayment',methods = ['GET','POST'])
def CreditCardRepayment():
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    return  render_template('CreditCardRepayment.html',username=client.username,balance=client.balance)