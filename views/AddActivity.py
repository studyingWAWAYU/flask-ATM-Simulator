import os.path

from flask import render_template,request,redirect, flash,session
from flask import Blueprint

from ATMflask import db, app
from ATMflask.sql import User

addAct = Blueprint('addAct',__name__)

@addAct.route('/',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def addActivity():
    user_id = session.get('id')
    username = None

    if user_id:
        user = User.query.get(user_id)
        username = user.username

    if request.method == 'GET':
        return render_template('AddActivity.html',username=username)

    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))


