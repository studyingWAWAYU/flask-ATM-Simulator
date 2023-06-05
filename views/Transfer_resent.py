from flask import Flask,render_template,request,redirect,session,flash
from flask import Blueprint
from ATMflask import db
from ATMflask.sql import User

TR = Blueprint('TR',__name__)


@TR.route('/Transfer_resent',methods = ['GET','POST'])
def Transfer_resent():
    if request.method == 'GET':
        return render_template('Transfer_resent.html')
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()

    return render_template('Transfer_resent.html')