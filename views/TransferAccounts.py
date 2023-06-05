from flask import Flask,render_template,request,redirect,session,flash
from flask import Blueprint
from ATMflask import db
from ATMflask.sql import User,app

TA = Blueprint('TA',__name__)

@TA.route('/TransferAccounts',methods = ['GET','POST'])
def TransferAccounts():
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    return  render_template('TransferAccounts.html',username=client.username,balance=client.balance)
