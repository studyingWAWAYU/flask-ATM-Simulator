from flask import Flask,render_template,request,redirect,session,flash
from flask import Blueprint
from ATMflask import db
from ATMflask.sql import User

mn = Blueprint("mn", __name__)

@mn.route('/menu',methods=['GET','POST'])
def menu():
    id = session.get('id')
    client = db.session.query(User).filter(User.id == id).first()
    return render_template('menu.html',username=client.username)



