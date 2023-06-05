from flask import Flask,render_template,request,redirect,session,flash
from flask import Blueprint
from ATMflask import db
from ATMflask.sql import User

FD = Blueprint('FD',__name__)

@FD.route('/FinancialDetail',methods = ['GET','POST'])
def FinancialDetail():
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    return  render_template('FinancialDetail.html',username=client.username,FinancialDetail=client.FinancialDetail)
