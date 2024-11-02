from flask import Blueprint
from flask import render_template, session

from ATMflask import db
from ATMflask.sql import User

mn = Blueprint("mn", __name__)

@mn.route('/menu',methods=['GET','POST'])
def menu():
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()
    return render_template('menu.html',username=client.username)



