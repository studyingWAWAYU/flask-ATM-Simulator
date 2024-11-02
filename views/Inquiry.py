from flask import Blueprint
from flask import render_template, redirect, session

from ATMflask import db
from ATMflask.sql import User

IQ = Blueprint('IQ',__name__)


@IQ.route('/Inquiry',methods = ['GET','POST'])
def Inquiry():
    user_info = session.get('user_info.py')
    if user_info:
        return redirect('/login')
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    return  render_template('Inquiry.html',username=client.username,detail=client.ICDetail)
