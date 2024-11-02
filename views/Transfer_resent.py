from flask import Blueprint
from flask import render_template, request, session

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