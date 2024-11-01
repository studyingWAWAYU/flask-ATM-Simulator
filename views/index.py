from flask import render_template,request,redirect, flash,session
from flask import Blueprint

from ATMflask import db
from ATMflask.sql import User

idx = Blueprint('idx',__name__)

@idx.route('/',methods = ['GET','POST'])  # 用装饰器定义路由的对应关系
def index():
    if request.method == 'GET':
        return render_template('index.html')