
from flask import Blueprint
from flask import render_template, session

from ATMflask import db
from ATMflask.sql import User

REC = Blueprint('REC',__name__)


@REC.route('/Recharge',methods = ['GET','POST'])
def Recharge():
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    return  render_template('Recharge.html',username=client.username,balance=client.balance)