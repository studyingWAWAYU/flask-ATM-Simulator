from flask import Blueprint
from flask import render_template, session

from ATMflask import db
from ATMflask.sql import User

FM = Blueprint('FM',__name__)


@FM.route('/FinancialManagement',methods = ['GET','POST'])
def FinancialManagement():
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()
    return render_template('FinancialManagement.html', username=client.username)
