from flask import Flask,render_template,request,redirect,session,flash
from flask import Blueprint
from ATMflask import db
from ATMflask.sql import User

FM = Blueprint('FM',__name__)


@FM.route('/FinancialManagement',methods = ['GET','POST'])
def FinancialManagement():
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()
    return render_template('FinancialManagement.html', username=client.username)
