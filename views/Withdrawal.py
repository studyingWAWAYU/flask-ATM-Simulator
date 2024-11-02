from flask import Blueprint
from flask import render_template, session

from ATMflask import db
from ATMflask.sql import User

WD = Blueprint('WD',__name__)


@WD.route('/Withdrawal',methods = ['GET','POST'])
def Withdrawal():
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()
    return  render_template('Withdrawal.html',username=client.username)
