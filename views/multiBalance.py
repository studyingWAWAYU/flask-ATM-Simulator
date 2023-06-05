from flask import Flask,render_template,request,redirect,session,flash
from flask import Blueprint
from ATMflask import db
from ATMflask.sql import User

MB = Blueprint('MB',__name__)


@MB.route('/multiBalance',methods = ['GET','POST'])
def multiBalance():
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    return  render_template('multiBalance.html',username=client.username,multiBalance=client.multiBalance)
