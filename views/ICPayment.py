
from flask import Blueprint
from flask import render_template, session

from ATMflask import db
from ATMflask.sql import User

ICP = Blueprint('ICP',__name__)


@ICP.route('/ICPayment',methods = ['GET','POST'])
def ICPayment():
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    return  render_template('ICPayment.html',username=client.username,balance=client.balance)